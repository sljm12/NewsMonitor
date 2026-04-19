from fastapi import FastAPI, Depends, Query
from sqlmodel import Session, select
from typing import List
from backend.database import init_db, get_session
from backend.models import Article
from backend.rss_service import fetch_and_store_feeds
from backend.extraction_service import process_unassessed_articles

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

@app.post("/feeds/extract")
def trigger_extraction():
    process_unassessed_articles()
    return {"message": "Entity extraction completed"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
