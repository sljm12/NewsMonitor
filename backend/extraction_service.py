import os
import json
from typing import List, Dict, Optional
from uuid import UUID
from openai import OpenAI
from sqlmodel import Session, select
from backend.models import Article, ExtractedEntity
from backend.database import engine
from backend.config import ARTICLE_CATEGORIES, ENTITY_TYPES

from dotenv import load_dotenv
load_dotenv(dotenv_path="backend/.env")

# Load configuration
API_KEY = os.getenv("LLM_API_KEY")
BASE_URL = os.getenv("LLM_BASE_URL", "https://api.openai.com/v1")
MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")

SYSTEM_PROMPT = f"""
You are a geopolitical intelligence analyst. Your task is to analyze news articles to provide a summary, classify the article, identify the primary event, and extract key entities.

Return a JSON object with:
1. 'summary': A high-signal, 2-3 sentence summary of the article focusing on geopolitical implications.
2. 'classification': Choose EXACTLY one category from this list: {", ".join(ARTICLE_CATEGORIES)}.
3. 'primary_event': The canonical name of the specific event this article is reporting on (e.g., '2026 G7 Summit', 'State Visit of Donald Trump to the UK'). 
   - If it matches an existing event from the provided list, use that EXACT name. 
   - Otherwise, propose a new, concise, and canonical name. 
   - If no specific event, use null.
4. 'main_country': The primary country the article is about. Use normalized name (e.g., 'United States' instead of 'US'). If no specific country, use null.
5. 'main_city': The primary city the article is about. Use normalized name. If no specific city, use null.
6. 'entities': A list of key entities mentioned. For locations, be as specific as possible (Country vs City).
   Each entity must have:
   - 'name': The normalized name of the entity (e.g., 'United States' instead of 'US', 'United Kingdom' instead of 'UK').
   - 'type': Must be EXACTLY one from this list: {", ".join(ENTITY_TYPES)}.
   - 'confidence': A float between 0.0 and 1.0 representing your certainty.

Respond ONLY with the JSON object.
"""

def analyze_article_content(article: Article, recent_events: List[str] = []) -> Dict:
    """Analyzes article content to generate a summary and extract entities."""
    # Ensure API key is available
    api_key = os.getenv("LLM_API_KEY")
    base_url = os.getenv("LLM_BASE_URL", "https://api.openai.com/v1")
    model = os.getenv("LLM_MODEL", "gpt-4o-mini")
    
    if not api_key:
        print(f"Skipping article {article.id}: No API key provided.")
        return {"summary": "", "entities": []}

    client = OpenAI(api_key=api_key, base_url=base_url)

    # Prioritize full_text (scraped content), fallback to rss_summary
    content_body = article.full_text if article.full_text else article.rss_summary
    if not content_body:
        content_body = "No content available."

    # Truncate content to avoid exceeding context limits (rough estimate for safety)
    max_chars = 12000 
    truncated_content = content_body[:max_chars]

    event_context = f"\nRecent Events to reconcile against: {', '.join(recent_events)}" if recent_events else ""
    content = f"Title: {article.title}\nContent: {truncated_content}{event_context}"
    
    try:
        response = client.chat.completions.create(
            model=model,  # Using local variable
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": content}
            ],
            extra_body={"reasoning": {"enabled": False}}
        )
        
        if not response or not response.choices:
            print(f"Error: Empty response or no choices from LLM for article {article.id}")
            return {"summary": "", "entities": []}

        result = json.loads(response.choices[0].message.content)
        return {
            "summary": result.get("summary", ""),
            "classification": result.get("classification", "Uncategorized"),
            "primary_event": result.get("primary_event"),
            "main_country": result.get("main_country"),
            "main_city": result.get("main_city"),
            "entities": result.get("entities", [])
        }
    except Exception as e:
        print(f"Error analyzing article {article.id}: {e}")
        return {"summary": "", "entities": []}

from backend.models import Article, ExtractedEntity, Event

def process_unassessed_articles(article_id: Optional[UUID] = None):
    with Session(engine) as session:
        # Fetch existing events for reconciliation
        existing_events = session.exec(select(Event)).all()
        recent_event_names = [e.name for e in existing_events]

        if article_id:
            # Fetch a specific article
            statement = select(Article).where(Article.id == article_id)
            articles = session.exec(statement).all()
        else:
            # Fetch articles where assessment_done is False, full_text is not null, and full_text is not empty
            statement = select(Article).where(
                Article.assessment_done == False,
                Article.full_text != None,
                Article.full_text != ""
            )
            articles = session.exec(statement).all()
        
        if not articles:
            print("No articles found to process.")
            return

        for article in articles:
            print(f"Analyzing article: {article.title}")
            analysis_result = analyze_article_content(article, recent_events=recent_event_names)
            
            summary = analysis_result.get("summary")
            classification = analysis_result.get("classification")
            primary_event_name = analysis_result.get("primary_event")
            main_country = analysis_result.get("main_country")
            main_city = analysis_result.get("main_city")
            entities = analysis_result.get("entities", [])
            
            # Safely handle None summary for printing
            display_summary = (summary or "")[:100]
            print(f"Generated Summary: {display_summary}...")
            print(f"Classification: {classification}")
            print(f"Primary Event: {primary_event_name}")
            print(f"Main Location: {main_city}, {main_country}")
            print(f"Extracted {len(entities)} entities.")

            # Handle Event Reconciliation/Creation
            if primary_event_name:
                # Case-insensitive find
                event = session.exec(
                    select(Event).where(Event.name.ilike(primary_event_name))
                ).first()
                
                if not event:
                    print(f"Creating new event: {primary_event_name}")
                    event = Event(name=primary_event_name)
                    session.add(event)
                    session.commit()
                    session.refresh(event)
                    # Add to the list for the next article in this batch
                    recent_event_names.append(event.name)
                
                article.event_id = event.id

            # Save the generated results
            article.summary = summary
            article.classification = classification
            article.main_country = main_country
            article.main_city = main_city
            
            # Save extracted entities
            for data in analysis_result.get("entities", []):
                entity = ExtractedEntity(
                    article_id=article.id,
                    entity_name=data.get("name"),
                    entity_type=data.get("type"),
                    confidence=data.get("confidence", 1.0)
                )
                session.add(entity)
            
            article.assessment_done = True
            session.add(article)
            session.commit()
            print(f"Successfully processed and committed article: {article.title}")

if __name__ == "__main__":
    # Test run
    process_unassessed_articles()
