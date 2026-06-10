import os
from sqlalchemy import text
from backend.database import engine
from dotenv import load_dotenv

load_dotenv(dotenv_path="backend/.env")

def migrate():
    with engine.connect() as connection:
        print("Starting cleanup migration: Removing deprecated tables and columns...")
        
        try:
            # 1. Drop hotspot table
            print("Dropping 'hotspot' table...")
            connection.execute(text("DROP TABLE IF EXISTS hotspot CASCADE;"))
            
            # 2. Drop articlehotspotlink table
            print("Dropping 'articlehotspotlink' table...")
            connection.execute(text("DROP TABLE IF EXISTS articlehotspotlink CASCADE;"))
            
            # 3. Drop event_id from article
            check_event_id_col = text("SELECT column_name FROM information_schema.columns WHERE table_name='article' AND column_name='event_id';")
            if connection.execute(check_event_id_col).fetchone():
                print("Dropping 'event_id' column from 'article'...")
                connection.execute(text("ALTER TABLE article DROP COLUMN event_id;"))
            
            connection.commit()
            print("Cleanup migration completed successfully.")
            
        except Exception as e:
            print(f"Error during cleanup migration: {e}")
            connection.rollback()
            raise e

if __name__ == "__main__":
    migrate()
