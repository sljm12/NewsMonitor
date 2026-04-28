import argparse
import os
import re
from datetime import datetime, time
from typing import Optional
from sqlmodel import Session, select, and_
from backend.models import Article
from backend.database import engine

def sanitize_filename(title: str) -> str:
    """Removes characters that are illegal in filenames."""
    # Remove \ / : * ? " < > |
    sanitized = re.sub(r'[\\/*?:"<>|]', "", title)
    # Replace spaces with underscores and limit length
    sanitized = sanitized.replace(" ", "_").strip("_")
    return sanitized[:100]

def export_articles(export_date_str: str, output_dir: str):
    """Exports articles published on a specific date to the output directory."""
    try:
        export_date = datetime.strptime(export_date_str, "%Y-%m-%d").date()
    except ValueError:
        print(f"Error: Invalid date format '{export_date_str}'. Use YYYY-MM-DD.")
        return

    # Define the start and end of the day
    start_of_day = datetime.combine(export_date, time.min)
    end_of_day = datetime.combine(export_date, time.max)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")

    with Session(engine) as session:
        statement = select(Article).where(
            and_(
                Article.published_at >= start_of_day,
                Article.published_at <= end_of_day,
                Article.full_text != None
            )
        )
        articles = session.exec(statement).all()

        if not articles:
            print(f"No articles with full text found for date: {export_date_str}")
            return

        print(f"Found {len(articles)} articles to export.")
        
        for article in articles:
            sanitized_title = sanitize_filename(article.title)
            filename = f"{article.id}_{sanitized_title}.md"
            file_path = os.path.join(output_dir, filename)

            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(f"# {article.title}\n\n")
                    f.write(f"Source: {article.source_url}\n")
                    f.write(f"Published: {article.published_at}\n")
                    f.write(f"Link: {article.link}\n\n")
                    f.write(article.full_text)
                print(f"Exported: {filename}")
            except Exception as e:
                print(f"Failed to export {article.id}: {e}")

    print("Export complete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export article full text to Markdown files.")
    parser.add_argument("--date", required=True, help="Date to export (YYYY-MM-DD)")
    parser.add_argument("--output-dir", default="export", help="Directory to save exported files (default: export)")

    args = parser.parse_args()
    export_articles(args.date, args.output_dir)
