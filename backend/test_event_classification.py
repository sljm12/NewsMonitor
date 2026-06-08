import os
from uuid import uuid4
from sqlmodel import Session, create_engine, SQLModel, select
from backend.models import Article, Event, EventReadWithArticles
from backend.main import enrich_article_with_coords

# Use an in-memory SQLite database for testing
engine = create_engine("sqlite://")
SQLModel.metadata.create_all(engine)

def test_event_classification_model():
    with Session(engine) as session:
        # 1. Test Event Creation with Classification
        event = Event(
            name="Test Geopolitical Event",
            description="A test event",
            classification="Geopolitics"
        )
        session.add(event)
        session.commit()
        session.refresh(event)
        
        assert event.classification == "Geopolitics"
        print(f"Event created with classification: {event.classification}")

        # 2. Test Article Linking to Event
        article = Article(
            title="Geopolitical News",
            link="http://example.com/news",
            source_url="http://example.com",
            event_id=event.id,
            classification="Geopolitics"
        )
        session.add(article)
        session.commit()
        session.refresh(article)
        
        assert article.event_id == event.id
        print(f"Article linked to event: {article.title}")

        # 3. Test Relationship and Schema
        # Simulate API response model
        event_from_db = session.exec(select(Event).where(Event.id == event.id)).first()
        event_read = EventReadWithArticles.model_validate(event_from_db)
        
        assert event_read.classification == "Geopolitics"
        assert len(event_read.articles) == 1
        assert event_read.articles[0].title == "Geopolitical News"
        print("Relationship and Schema validation passed!")

if __name__ == "__main__":
    try:
        test_event_classification_model()
        print("All event classification tests passed!")
    except Exception as e:
        print(f"Tests failed with error: {e}")
        import traceback
        traceback.print_exc()
