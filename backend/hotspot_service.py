import os
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from uuid import UUID
from openai import OpenAI
from sqlmodel import Session, select, delete
from backend.models import Article, HotSpot, Country, GeoName
from backend.database import engine
from backend.config import ARTICLE_CATEGORIES

from dotenv import load_dotenv
load_dotenv(dotenv_path="backend/.env")

# Load configuration
API_KEY = os.getenv("LLM_API_KEY")
BASE_URL = os.getenv("LLM_BASE_URL", "https://api.openai.com/v1")
MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")

import re

HOTSPOT_SYSTEM_PROMPT = f"""
You are a senior geopolitical risk analyst. Your task is to identify the most significant "Hot Spots" around the world based on recent news. 

A "Hot Spot" is a location experiencing a high-intensity event such as a war, conflict, health pandemic, coup, or major civil unrest.

Based on the provided article summaries, identify the top 5-10 active Hot Spots.
For each Hot Spot, provide:
1. 'name': A concise, canonical name for the situation (e.g., 'Sudan Civil War', 'Marburg Virus Outbreak in Rwanda').
2. 'description': A high-signal situation report (3-4 sentences) explaining the current status and implications.
3. 'category': Choose EXACTLY one category from this list: {", ".join(ARTICLE_CATEGORIES)}.
4. 'severity': An integer from 1 to 10 (10 being most severe/global impact).
5. 'location_name': The primary city or region and country (e.g., 'Khartoum, Sudan').
6. 'main_country': The primary country.
7. 'main_city': The primary city (if applicable, else null).
8. 'source_article_ids': A list of the EXACT article UUID strings (found in the square brackets [ ]) that provided the information for this Hot Spot.

Return a JSON object with a key 'hotspots' containing the list of Hot Spot objects.
Respond ONLY with the JSON object.
"""

def clean_uuid(id_str: str) -> Optional[str]:
    """Extracts a valid UUID string from a potentially messy LLM response."""
    if not id_str:
        return None
    # Regex for a standard UUID (8-4-4-4-12 hex digits)
    uuid_pattern = re.compile(r'[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}')
    match = uuid_pattern.search(id_str)
    return match.group(0) if match else None

def refresh_hotspots():
    """Identifies and updates global hotspots based on recent high-impact news."""
    if not API_KEY:
        print("No API key provided for HotSpot identification.")
        return

    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
    
    with Session(engine) as session:
        # 1. Fetch high-impact articles from the last 72 hours
        three_days_ago = datetime.utcnow() - timedelta(days=3)
        statement = select(Article).where(
            Article.published_at >= three_days_ago,
            Article.assessment_done == True,
            Article.classification.in_(["Conflict/War", "Health", "Internal Politics", "Human Rights", "Crime"])
        )
        articles = session.exec(statement).all()
        
        if not articles:
            print("No recent high-impact articles found to analyze for hotspots.")
            return

        # 2. Prepare article data for LLM
        # Grouping by location to reduce token usage and provide better context
        location_groups = {}
        print(f"Analyzing {len(articles)} articles for hotspots...")
        for a in articles:
            loc = f"{a.main_city}, {a.main_country}" if a.main_city else a.main_country
            if loc not in location_groups:
                location_groups[loc] = []
            location_groups[loc].append(f"[{a.id}] {a.title} | {a.summary}")

        input_data = []
        for loc, summaries in location_groups.items():
            input_data.append(f"Location: {loc}\n" + "\n".join(summaries[:5])) # Limit to 5 summaries per location

        prompt_content = "\n\n".join(input_data)
        # print(f"DEBUG Prompt Content:\n{prompt_content[:500]}...")
        
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": HOTSPOT_SYSTEM_PROMPT},
                    {"role": "user", "content": f"Analyze these recent news items and identify the primary Hot Spots:\n\n{prompt_content}"}
                ],
                response_format={"type": "json_object"}
            )
            
            raw_content = response.choices[0].message.content
            result = json.loads(raw_content)
            hotspots_data = result.get("hotspots", [])
            
            # 3. Update Database
            # Deactivate current hotspots
            session.exec(delete(HotSpot))
            session.commit()

            for data in hotspots_data:
                # Resolve coordinates
                lat, lon = 0.0, 0.0
                country_name = data.get("main_country")
                city_name = data.get("main_city")

                # Try to get coordinates from Country/GeoName tables
                country = session.exec(select(Country).where(Country.name == country_name)).first()
                if country:
                    lat, lon = country.latitude, country.longitude
                    if city_name:
                        city = session.exec(
                            select(GeoName)
                            .where(GeoName.name == city_name)
                            .where(GeoName.country_code == country.alpha2)
                            .order_by(GeoName.population.desc())
                        ).first()
                        if city:
                            lat, lon = city.latitude, city.longitude

                # Fetch linked articles
                source_ids = data.get("source_article_ids", [])
                linked_articles = []
                for s_id in source_ids:
                    cleaned_id = clean_uuid(s_id)
                    if cleaned_id:
                        try:
                            article_uuid = UUID(cleaned_id)
                            article = session.get(Article, article_uuid)
                            if article:
                                linked_articles.append(article)
                        except (ValueError, TypeError):
                            continue
                
                hotspot = HotSpot(
                    name=data.get("name"),
                    description=data.get("description"),
                    category=data.get("category"),
                    severity=data.get("severity", 5),
                    location_name=data.get("location_name"),
                    latitude=lat,
                    longitude=lon,
                    is_active=True,
                    articles=linked_articles
                )
                session.add(hotspot)
            
            session.commit()
            print(f"Successfully updated {len(hotspots_data)} hotspots.")

        except Exception as e:
            print(f"Error during HotSpot identification: {e}")

if __name__ == "__main__":
    refresh_hotspots()
