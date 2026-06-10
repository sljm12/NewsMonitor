import os
from sqlalchemy import text
from backend.database import engine
from dotenv import load_dotenv

load_dotenv(dotenv_path="backend/.env")

def migrate():
    with engine.connect() as connection:
        print("Starting migration: Unifying Events and Hotspots...")
        
        try:
            # 1. Add new columns to 'event' table
            cols_to_add = [
                ("category", "VARCHAR"),
                ("severity", "INTEGER DEFAULT 5"),
                ("location_name", "VARCHAR"),
                ("latitude", "DOUBLE PRECISION"),
                ("longitude", "DOUBLE PRECISION"),
                ("is_active", "BOOLEAN DEFAULT TRUE"),
                ("is_hotspot", "BOOLEAN DEFAULT FALSE"),
                ("updated_at", "TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
            ]
            
            for col_name, col_type in cols_to_add:
                check_sql = text(f"SELECT column_name FROM information_schema.columns WHERE table_name='event' AND column_name='{col_name}';")
                result = connection.execute(check_sql).fetchone()
                if not result:
                    print(f"Adding column '{col_name}' to 'event'...")
                    connection.execute(text(f"ALTER TABLE event ADD COLUMN {col_name} {col_type};"))
                else:
                    print(f"Column '{col_name}' already exists in 'event'.")
            
            # 2. Create 'articleeventlink' table
            connection.execute(text("""
                CREATE TABLE IF NOT EXISTS articleeventlink (
                    article_id UUID NOT NULL,
                    event_id UUID NOT NULL,
                    PRIMARY KEY (article_id, event_id),
                    FOREIGN KEY(article_id) REFERENCES article (id) ON DELETE CASCADE,
                    FOREIGN KEY(event_id) REFERENCES event (id) ON DELETE CASCADE
                );
            """))
            print("Table 'articleeventlink' verified/created.")

            # 3. Migrate HotSpot records to Event
            # Check if hotspot table exists first
            check_hotspot_table = text("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'hotspot');")
            if connection.execute(check_hotspot_table).scalar():
                hotspots = connection.execute(text("SELECT * FROM hotspot")).fetchall()
                print(f"Found {len(hotspots)} hotspots to migrate.")
                for hs in hotspots:
                    name = hs.name
                    # Check if event with this name exists
                    existing_event = connection.execute(text("SELECT id FROM event WHERE name = :name"), {"name": name}).fetchone()
                    
                    if not existing_event:
                        print(f"Migrating hotspot '{name}' to event...")
                        connection.execute(text("""
                            INSERT INTO event (id, name, description, category, severity, location_name, latitude, longitude, is_active, is_hotspot, created_at, updated_at)
                            VALUES (:id, :name, :description, :category, :severity, :location_name, :latitude, :longitude, :is_active, TRUE, :created_at, :updated_at)
                        """), {
                            "id": hs.id,
                            "name": hs.name,
                            "description": hs.description,
                            "category": hs.category,
                            "severity": hs.severity,
                            "location_name": hs.location_name,
                            "latitude": hs.latitude,
                            "longitude": hs.longitude,
                            "is_active": hs.is_active,
                            "created_at": hs.created_at,
                            "updated_at": hs.updated_at
                        })
                        event_id = hs.id
                    else:
                        event_id = existing_event.id
                        print(f"Event '{name}' already exists, updating with hotspot data...")
                        connection.execute(text("""
                            UPDATE event SET 
                                is_hotspot = TRUE,
                                category = COALESCE(category, :category),
                                severity = :severity,
                                location_name = :location_name,
                                latitude = :latitude,
                                longitude = :longitude,
                                is_active = :is_active,
                                updated_at = :updated_at
                            WHERE id = :id
                        """), {
                            "id": event_id,
                            "category": hs.category,
                            "severity": hs.severity,
                            "location_name": hs.location_name,
                            "latitude": hs.latitude,
                            "longitude": hs.longitude,
                            "is_active": hs.is_active,
                            "updated_at": hs.updated_at
                        })

                    # 4. Migrate ArticleHotSpotLink to ArticleEventLink
                    # Check if articlehotspotlink table exists
                    check_link_table = text("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'articlehotspotlink');")
                    if connection.execute(check_link_table).scalar():
                        links = connection.execute(text("SELECT article_id FROM articlehotspotlink WHERE hotspot_id = :hs_id"), {"hs_id": hs.id}).fetchall()
                        for link in links:
                            connection.execute(text("""
                                INSERT INTO articleeventlink (article_id, event_id)
                                VALUES (:article_id, :event_id)
                                ON CONFLICT DO NOTHING
                            """), {"article_id": link.article_id, "event_id": event_id})
            else:
                print("Table 'hotspot' does not exist, skipping hotspot migration.")

            # 5. Migrate Article.event_id to ArticleEventLink
            # Check if event_id column exists in article table
            check_event_id_col = text("SELECT column_name FROM information_schema.columns WHERE table_name='article' AND column_name='event_id';")
            if connection.execute(check_event_id_col).fetchone():
                articles_with_events = connection.execute(text("SELECT id, event_id FROM article WHERE event_id IS NOT NULL")).fetchall()
                print(f"Migrating {len(articles_with_events)} article-event links from article.event_id...")
                for art in articles_with_events:
                    connection.execute(text("""
                        INSERT INTO articleeventlink (article_id, event_id)
                        VALUES (:article_id, :event_id)
                        ON CONFLICT DO NOTHING
                    """), {"article_id": art.id, "event_id": art.event_id})
            
            connection.commit()
            print("Migration completed successfully.")
            
        except Exception as e:
            print(f"Error during migration: {e}")
            connection.rollback()
            raise e

if __name__ == "__main__":
    migrate()
