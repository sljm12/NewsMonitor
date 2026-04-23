from fastapi import FastAPI, Depends, Query
from sqlmodel import Session, select
from typing import List, Optional
from uuid import UUID
from backend.database import init_db, get_session
from backend.models import Article
from backend.rss_service import fetch_and_store_feeds
from backend.extraction_service import process_unassessed_articles
from backend.crawler_service import process_pending_crawls

app = FastAPI(title="Global Pulse API")

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
    limit: int = Query(default=100, le=100),
    session: Session = Depends(get_session)
):
    articles = session.exec(select(Article).order_by(Article.published_at.desc()).offset(offset).limit(limit)).all()
    return articles

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
