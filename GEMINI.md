# GEMINI.md - Global Pulse Project Context

## Project Overview
**Global Pulse** is a real-time, automated RSS feed processor designed to provide high-signal geopolitical awareness. It identifies key locations, organizations, and significant events from diverse news sources and presents them in a centralized "Intelligence Dashboard."

### Architecture
- **Backend:** Python-based FastAPI application.
- **Database:** SQLModel (ORM) used with PostgreSQL.
- **RSS Parsing:** `feedparser` handles external feed ingestion.
- **Frontend:** (Planned) React 18+ with TypeScript and Vite, featuring a dark "Command Center" aesthetic.

### Future Scaling (Planned)
- **Task Queue:** Redis/Celery for distributed processing.
- **Distributed Crawling:** Decoupled workers running Crawl4AI to handle high-volume ingestions.

## Tech Stack
- **Languages:** Python (Backend), TypeScript (Frontend).
- **Frameworks:** FastAPI, React.
- **Storage:** PostgreSQL via SQLModel.
- **Key Libraries:** `feedparser`, `crawl4ai`, `uvicorn`, `sqlmodel`, `psycopg2-binary`.

## Getting Started

### Backend Setup
1. **Environment:** Use Python 3.10+.
2. **Install Dependencies:**
   ```bash
   pip install -r backend/requirements.txt
   ```
3. **Configuration:** Ensure `backend/.env` is configured with necessary database credentials and environment variables.
4. **Initialize Database:** The application initializes the database automatically on startup via `init_db()`.
5. **Run the Server:**
   ```bash
   python -m backend.main
   ```
   The API will be available at `http://localhost:8000`.

### Feed Configuration
- RSS feed URLs are managed in `links.txt` at the project root.
- The system fetches and stores new articles from these links on startup or via the `/feeds/refresh` endpoint.

## Development Conventions

### Coding Standards
- **Python:** Follow PEP 8. Use explicit type hints with SQLModel.
- **Models:** All database models must be defined in `backend/models.py`.
- **API Design:** RESTful endpoints should be defined in `backend/main.py`.

### Testing
- [TODO] Add automated test suite for RSS parsing and entity extraction.

### Entity Extraction & Summarization
- Uses an LLM-based approach (OpenAI, OpenRouter, or LM Studio) to identify locations, organizations, and events.
- **Summarization:** The LLM generates a high-signal 2-3 sentence summary based on the `full_text` of the article (fetched via Crawl4AI) rather than the short RSS summary.
- Configuration is managed via `.env` (`LLM_API_KEY`, `LLM_BASE_URL`, `LLM_MODEL`).
- Triggered via the `/feeds/extract` API endpoint or running `backend/extraction_service.py` directly.
- Entities are linked to `Article` records via the `ExtractedEntity` model.

## Development Notes

### Shell & CLI
- **PowerShell Compatibility:** When chaining commands (e.g., Git operations), use `;` instead of `&&`.
  - *Correct:* `git add .; git commit -m "message"`
  - *Incorrect:* `git add . && git commit -m "message"`

### Key Files

- `backend/main.py`: Application entry point and API routes.
- `backend/models.py`: Database schema definitions (Articles, Entities).
- `backend/rss_service.py`: Logic for fetching and parsing RSS feeds.
- `backend/crawler_service.py`: Logic for full-text article scraping using Crawl4AI.
- `backend/extraction_service.py`: LLM-based entity extraction logic.
- `specs/`: Contains mission, roadmap, and technical specifications.
- `links.txt`: List of RSS feed URLs to monitor.
