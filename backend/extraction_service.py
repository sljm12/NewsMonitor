import os
import json
from typing import List, Dict
from openai import OpenAI
from sqlmodel import Session
from backend.models import Article, ExtractedEntity
from backend.database import engine

# Load configuration
API_KEY = os.getenv("LLM_API_KEY", "sk-...")
BASE_URL = os.getenv("LLM_BASE_URL", "https://api.openai.com/v1")
MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

SYSTEM_PROMPT = """
You are a geopolitical intelligence analyst. Your task is to extract entities from news articles.
Return a JSON object with a list of 'entities'.
Each entity must have:
- 'name': The name of the entity.
- 'type': One of 'Location', 'Organization', or 'Event'.
- 'confidence': A float between 0.0 and 1.0 representing your certainty.

Respond ONLY with the JSON object.
"""

def extract_entities_for_article(article: Article) -> List[Dict]:
    content = f"Title: {article.title}\nSummary: {article.summary}"
    
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": content}
            ],
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
        return result.get("entities", [])
    except Exception as e:
        print(f"Error extracting entities for article {article.id}: {e}")
        return []

def process_unassessed_articles():
    with Session(engine) as session:
        # Fetch articles where assessment_done is False
        from sqlmodel import select
        statement = select(Article).where(Article.assessment_done == False)
        articles = session.exec(statement).all()
        
        for article in articles:
            print(f"Processing article: {article.title}")
            entities_data = extract_entities_for_article(article)
            
            for data in entities_data:
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
