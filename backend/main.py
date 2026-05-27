from fastapi import FastAPI, Depends, Query, HTTPException
from sqlmodel import Session, select, delete, update
from sqlalchemy.orm import selectinload
from typing import List, Optional
from uuid import UUID
from backend.database import init_db, get_session
from backend.models import Article, ExtractedEntity, ArticleReadWithEntities, Country, GeoName, Event, HotSpot
from backend.rss_service import fetch_and_store_feeds
from backend.extraction_service import process_unassessed_articles
from backend.crawler_service import process_pending_crawls
from backend.hotspot_service import refresh_hotspots

app = FastAPI(title="Global Pulse API")

def enrich_article_with_coords(article: Article, session: Session) -> ArticleReadWithEntities:
    """Enriches an article with latitude and longitude based on its main location and includes event name."""
    # Use model_validate for SQLModel/Pydantic v2 compatibility
    result = ArticleReadWithEntities.model_validate(article)
    
    # Add event name if available
    if article.event_id:
        event = session.get(Event, article.event_id)
        if event:
            result.event_name = event.name

    if not article.main_country:
        return result

    # 1. Lookup Country to get alpha2 and default coords
    country = session.exec(select(Country).where(Country.name == article.main_country)).first()
    if not country:
        return result

    # Default to country coordinates
    result.latitude = country.latitude
    result.longitude = country.longitude

    # 2. If city is present, try to find more granular coordinates in GeoNames
    if article.main_city:
        # Highest population heuristic for ambiguous city names
        city = session.exec(
            select(GeoName)
            .where(GeoName.name == article.main_city)
            .where(GeoName.country_code == country.alpha2)
            .order_by(GeoName.population.desc())
        ).first()
        
        if city:
            result.latitude = city.latitude
            result.longitude = city.longitude

    return result

@app.on_event("startup")
def on_startup():
    init_db()
    # Initial fetch
    try:
        fetch_and_store_feeds()
    except Exception as e:
        print(f"Initial fetch failed: {e}")

@app.get("/feeds", response_model=List[Article])
def read_feeds(
    offset: int = 0,
    limit: int = Query(default=100, le=1000),
    session: Session = Depends(get_session)
):
    articles = session.exec(select(Article).order_by(Article.published_at.desc()).offset(offset).limit(limit)).all()
    return articles

@app.get("/articles", response_model=List[ArticleReadWithEntities])
@app.get("/assessment", response_model=List[ArticleReadWithEntities])
def read_articles(
    offset: int = 0,
    limit: int = Query(default=100, le=1000),
    article_id: Optional[UUID] = Query(default=None),
    session: Session = Depends(get_session)
):
    statement = select(Article).options(selectinload(Article.entities)).order_by(Article.published_at.desc())
    if article_id:
        statement = statement.where(Article.id == article_id)
    
    articles = session.exec(statement.offset(offset).limit(limit)).all()
    return [enrich_article_with_coords(article, session) for article in articles]

@app.get("/articles/{article_id}", response_model=ArticleReadWithEntities)
def read_article(article_id: UUID, session: Session = Depends(get_session)):
    article = session.exec(
        select(Article)
        .options(selectinload(Article.entities))
        .where(Article.id == article_id)
    ).first()
    
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return enrich_article_with_coords(article, session)

@app.get("/events", response_model=List[Event])
def read_events(
    offset: int = 0,
    limit: int = Query(default=100, le=1000),
    session: Session = Depends(get_session)
):
    events = session.exec(select(Event).order_by(Event.created_at.desc()).offset(offset).limit(limit)).all()
    return events

@app.get("/events/{event_id}", response_model=Event)
def read_event(event_id: UUID, session: Session = Depends(get_session)):
    event = session.exec(
        select(Event)
        .options(selectinload(Event.articles))
        .where(Event.id == event_id)
    ).first()
    
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@app.post("/feeds/refresh")
def refresh_feeds():
    fetch_and_store_feeds()
    return {"message": "Feeds refreshed successfully"}

@app.post("/feeds/crawl")
async def trigger_crawl(article_id: Optional[UUID] = Query(default=None)):
    await process_pending_crawls(article_id=article_id)
    return {"message": "Crawl processing completed"}

@app.post("/feeds/extract")
def trigger_extraction(article_id: Optional[UUID] = Query(default=None)):
    process_unassessed_articles(article_id=article_id)
    return {"message": "Entity extraction completed"}

@app.post("/articles/{article_id}/reset")
def reset_article(
    article_id: UUID,
    clear_full_text: bool = Query(default=False),
    session: Session = Depends(get_session)
):
    article = session.get(Article, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    # Delete associated entities
    session.exec(delete(ExtractedEntity).where(ExtractedEntity.article_id == article_id))

    # Reset article fields
    article.summary = None
    article.assessment_done = False
    article.classification = None
    if clear_full_text:
        article.full_text = None

    session.add(article)
    session.commit()
    session.refresh(article)

    return {"message": f"Article {article_id} reset successfully", "article": article}

class HotSpotReadWithArticles(SQLModel):
    id: UUID
    name: str
    description: str
    category: Optional[str]
    severity: int
    location_name: str
    latitude: float
    longitude: float
    is_active: bool
    created_at: datetime
    updated_at: datetime
    articles: List[Article] = []

@app.get("/hotspots", response_model=List[HotSpotReadWithArticles])
def get_hotspots(session: Session = Depends(get_session)):
    hotspots = session.exec(
        select(HotSpot)
        .options(selectinload(HotSpot.articles))
        .where(HotSpot.is_active == True)
        .order_by(HotSpot.severity.desc())
    ).all()
    return hotspots

@app.post("/hotspots/refresh")
def trigger_hotspot_refresh():
    refresh_hotspots()
    return {"message": "HotSpot identification completed"}

@app.post("/articles/reset-all")
def reset_all_articles(
    clear_full_text: bool = Query(default=False),
    session: Session = Depends(get_session)
):
    # Delete all associated entities
    session.exec(delete(ExtractedEntity))

    # Prepare update statement
    statement = update(Article).values(
        summary=None,
        assessment_done=False,
        classification=None
    )
    if clear_full_text:
        statement = statement.values(full_text=None)

    # Execute bulk update
    session.exec(statement)
    session.commit()

    return {"message": "All articles reset successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
