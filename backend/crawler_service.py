import asyncio
from typing import Optional
from uuid import UUID
from crawl4ai import AsyncWebCrawler
from sqlmodel import Session, select
from backend.models import Article
from backend.database import engine

async def crawl_article(url: str) -> str:
    """Crawls a single article and returns its markdown content."""
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url=url)
        return result.markdown

async def process_pending_crawls(article_id: Optional[UUID] = None):
    """Fetches articles without full_text and crawls them. 
    If article_id is provided, only crawls that specific article.
    """
    with Session(engine) as session:
        if article_id:
            statement = select(Article).where(Article.id == article_id)
        else:
            statement = select(Article).where(Article.full_text == None)
            
        articles = session.exec(statement).all()
        
        for article in articles:
            print(f"Crawling: {article.title}")
            try:
                markdown = await crawl_article(article.link)
                article.full_text = markdown
                session.add(article)
                session.commit()
            except Exception as e:
                print(f"Failed to crawl {article.link}: {e}")

if __name__ == "__main__":
    asyncio.run(process_pending_crawls())
