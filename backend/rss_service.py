import feedparser
from datetime import datetime
from time import mktime
from sqlmodel import Session, select
from backend.models import Article
from backend.database import engine

def fetch_and_store_feeds(links_file: str = "links.txt"):
    with open(links_file, "r") as f:
        urls = [line.strip() for line in f if line.strip()]

    with Session(engine) as session:
        for url in urls:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                # Check if article already exists
                statement = select(Article).where(Article.link == entry.link)
                existing_article = session.exec(statement).first()

                if not existing_article:
                    published = None
                    if hasattr(entry, 'published_parsed'):
                        published = datetime.fromtimestamp(mktime(entry.published_parsed))
                    
                    new_article = Article(
                        title=entry.get('title', 'No Title'),
                        link=entry.link,
                        summary=entry.get('summary', ''),
                        published_at=published,
                        source_url=url
                    )
                    session.add(new_article)
        
        session.commit()

if __name__ == "__main__":
    # Test run
    fetch_and_store_feeds()
