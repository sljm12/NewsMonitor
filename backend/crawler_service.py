import asyncio
import os
from typing import Optional
from uuid import UUID
from dotenv import load_dotenv
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig
from sqlmodel import Session, select
from backend.models import Article
from backend.database import engine

load_dotenv()

CRAWL4AI_DEBUG = os.getenv("CRAWL4AI_DEBUG", "false").lower() == "true"
CRAWL4AI_WAIT_TIME = int(os.getenv("CRAWL4AI_WAIT_TIME", "0"))

async def crawl_article(url: str) -> str:
    """Crawls a single article and returns its markdown content."""
    # headless=False shows the browser window when debug is enabled
    config= BrowserConfig(headless=not CRAWL4AI_DEBUG)

    async with AsyncWebCrawler(config=config) as crawler:
        # sleep_before_extract (or similar) adds a delay to allow dynamic content to load
        crawler_config= CrawlerRunConfig(delay_before_return_html=CRAWL4AI_WAIT_TIME)
        result = await crawler.arun(url=url, config=crawler_config)
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
                
                # Log first 100 characters
                preview = markdown[:100].replace('\n', ' ')
                print(f"Success! Preview: {preview}...")
                
                session.add(article)
                session.commit()
            except Exception as e:
                print(f"Failed to crawl {article.link}: {e}")

if __name__ == "__main__":
    asyncio.run(process_pending_crawls())
