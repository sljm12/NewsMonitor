import os
from sqlalchemy import text
from backend.database import engine
from dotenv import load_dotenv

load_dotenv(dotenv_path="backend/.env")

def migrate():
    """Adds main_country and main_city columns to the article table."""
    with engine.connect() as connection:
        print("Starting migration: Adding main_country and main_city columns to 'article' table...")
        
        try:
            # Check if main_country already exists to avoid errors on re-run
            check_sql = text("SELECT column_name FROM information_schema.columns WHERE table_name='article' AND column_name='main_country';")
            result = connection.execute(check_sql).fetchone()
            
            if not result:
                connection.execute(text("ALTER TABLE article ADD COLUMN main_country VARCHAR;"))
                connection.execute(text("CREATE INDEX ix_article_main_country ON article (main_country);"))
                print("Added column 'main_country' and its index.")
            else:
                print("Column 'main_country' already exists.")

            # Check if main_city already exists
            check_sql = text("SELECT column_name FROM information_schema.columns WHERE table_name='article' AND column_name='main_city';")
            result = connection.execute(check_sql).fetchone()
            
            if not result:
                connection.execute(text("ALTER TABLE article ADD COLUMN main_city VARCHAR;"))
                connection.execute(text("CREATE INDEX ix_article_main_city ON article (main_city);"))
                print("Added column 'main_city' and its index.")
            else:
                print("Column 'main_city' already exists.")
            
            connection.commit()
            print("Migration completed successfully.")
            
        except Exception as e:
            print(f"Error during migration: {e}")
            connection.rollback()

if __name__ == "__main__":
    migrate()
