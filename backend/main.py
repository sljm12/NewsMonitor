from fastapi import FastAPI, Depends, Query, HTTPException
from sqlmodel import Session, select, delete
from typing import List, Optional
from uuid import UUID
from backend.database import init_db, get_session
from backend.models import Article, ExtractedEntity
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
    if clear_full_text:
        article.full_text = None

    session.add(article)
    session.commit()
    session.refresh(article)

    return {"message": f"Article {article_id} reset successfully", "article": article}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
