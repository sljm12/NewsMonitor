import os
from sqlalchemy import text
from backend.database import engine
from dotenv import load_dotenv

load_dotenv(dotenv_path="backend/.env")

def migrate():
    """Creates the articlehotspotlink join table."""
    with engine.connect() as connection:
        print("Starting migration: Creating 'articlehotspotlink' table...")
        
        try:
            # Create table if it doesn't exist
            create_table_sql = text("""
                CREATE TABLE IF NOT EXISTS articlehotspotlink (
                    article_id UUID NOT NULL, 
                    hotspot_id UUID NOT NULL, 
                    PRIMARY KEY (article_id, hotspot_id), 
                    FOREIGN KEY(article_id) REFERENCES article (id), 
                    FOREIGN KEY(hotspot_id) REFERENCES hotspot (id)
                );
            """)
            connection.execute(create_table_sql)
            print("Table 'articlehotspotlink' verified/created.")
            
            connection.commit()
            print("Migration completed successfully.")
            
        except Exception as e:
            print(f"Error during migration: {e}")
            connection.rollback()

if __name__ == "__main__":
    migrate()
