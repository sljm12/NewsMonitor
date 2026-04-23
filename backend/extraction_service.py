import os
import json
from typing import List, Dict, Optional
from uuid import UUID
from openai import OpenAI
from sqlmodel import Session, select
from backend.models import Article, ExtractedEntity
from backend.database import engine

from dotenv import load_dotenv
load_dotenv(dotenv_path="backend/.env")

# Load configuration
API_KEY = os.getenv("LLM_API_KEY")
BASE_URL = os.getenv("LLM_BASE_URL", "https://api.openai.com/v1")
MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")

SYSTEM_PROMPT = """
You are a geopolitical intelligence analyst. Your task is to analyze news articles to provide a summary and extract key entities.

Return a JSON object with:
1. 'summary': A high-signal, 2-3 sentence summary of the article focusing on geopolitical implications.
2. 'entities': A list of entities found. Each entity must have:
   - 'name': The name of the entity.
   - 'type': One of 'Location', 'Organization', or 'Event'.
   - 'confidence': A float between 0.0 and 1.0 representing your certainty.

Respond ONLY with the JSON object.
"""

def analyze_article_content(article: Article) -> Dict:
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

    content = f"Title: {article.title}\nContent: {truncated_content}"
    
    try:
        response = client.chat.completions.create(
            model=model,  # Using local variable
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": content}
            ]
        )
        
        if not response or not response.choices:
            print(f"Error: Empty response or no choices from LLM for article {article.id}")
            return {"summary": "", "entities": []}

        result = json.loads(response.choices[0].message.content)
        return {
            "summary": result.get("summary", ""),
            "entities": result.get("entities", [])
        }
    except Exception as e:
        print(f"Error analyzing article {article.id}: {e}")
        return {"summary": "", "entities": []}

def process_unassessed_articles(article_id: Optional[UUID] = None):
    with Session(engine) as session:
        if article_id:
            # Fetch a specific article
            statement = select(Article).where(Article.id == article_id)
            articles = session.exec(statement).all()
        else:
            # Fetch articles where assessment_done is False
            statement = select(Article).where(Article.assessment_done == False)
            articles = session.exec(statement).all()
        
        if not articles:
            print("No articles found to process.")
            return

        for article in articles:
            print(f"Analyzing article: {article.title}")
            analysis_result = analyze_article_content(article)
            
            summary = analysis_result.get("summary")
            entities = analysis_result.get("entities", [])
            print(f"Generated Summary: {summary[:100]}...")
            print(f"Extracted {len(entities)} entities.")

            # Save the generated summary
            article.summary = summary
            
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

if __name__ == "__main__":
    # Test run
    process_unassessed_articles()
