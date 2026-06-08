import os
from sqlalchemy import text
from backend.database import engine
from dotenv import load_dotenv

load_dotenv(dotenv_path="backend/.env")

def migrate():
    """Adds classification column to the event table."""
    with engine.connect() as connection:
        print("Starting migration: Adding classification column to 'event' table...")
        
        try:
            # Check if classification already exists to avoid errors on re-run
            # Note: SQLModel uses lowercase table names by default, so 'event'
            check_sql = text("SELECT column_name FROM information_schema.columns WHERE table_name='event' AND column_name='classification';")
            result = connection.execute(check_sql).fetchone()
            
            if not result:
                connection.execute(text("ALTER TABLE event ADD COLUMN classification VARCHAR;"))
                connection.execute(text("CREATE INDEX ix_event_classification ON event (classification);"))
                print("Added column 'classification' and its index.")
            else:
                print("Column 'classification' already exists.")
            
            connection.commit()
            print("Migration completed successfully.")
            
        except Exception as e:
            print(f"Error during migration: {e}")
            connection.rollback()

if __name__ == "__main__":
    migrate()
