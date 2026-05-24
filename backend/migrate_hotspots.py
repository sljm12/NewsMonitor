import os
from sqlalchemy import text
from backend.database import engine
from dotenv import load_dotenv

load_dotenv(dotenv_path="backend/.env")

def migrate():
    """Adds category column to the hotspot table."""
    with engine.connect() as connection:
        print("Starting migration: Adding category column to 'hotspot' table...")
        
        try:
            # Check if category already exists to avoid errors on re-run
            check_sql = text("SELECT column_name FROM information_schema.columns WHERE table_name='hotspot' AND column_name='category';")
            result = connection.execute(check_sql).fetchone()
            
            if not result:
                connection.execute(text("ALTER TABLE hotspot ADD COLUMN category VARCHAR;"))
                connection.execute(text("CREATE INDEX ix_hotspot_category ON hotspot (category);"))
                print("Added column 'category' and its index.")
            else:
                print("Column 'category' already exists.")
            
            connection.commit()
            print("Migration completed successfully.")
            
        except Exception as e:
            print(f"Error during migration: {e}")
            connection.rollback()

if __name__ == "__main__":
    migrate()
