# Global Pulse

**Global Pulse** is a real-time, automated RSS feed processor designed to provide high-signal geopolitical awareness. It identifies key locations, organizations, and significant events from diverse news sources and presents them in a centralized "Intelligence Dashboard."

## 🚀 Overview

The system monitors a curated list of RSS feeds, scrapes full-text content using advanced crawlers, and utilizes LLMs to extract entities (locations, organizations, events) and generate concise, high-signal summaries. The goal is to provide an authoritative, precise, and vigilant interface for rapid data synthesis and situational awareness.

### Key Features

- **Automated Ingestion:** Regularly fetches articles from configured RSS feeds.
- **Full-Text Scraping:** Uses `Crawl4AI` to retrieve the complete content of news articles, moving beyond limited RSS snippets.
- **LLM-Powered Extraction:** Identifies geopolitical entities and significant events using modern LLMs.
- **High-Signal Summarization:** Generates 2-3 sentence summaries focused on intelligence value.
- **Intelligence Dashboard:** (Planned) A "Command Center" aesthetic interface for real-time monitoring.
- **Data Export:** Export processed data to Markdown or other formats for offline analysis.

## 🛠️ Tech Stack

### Backend
- **Framework:** [FastAPI](https://fastapi.tiangolo.com/) (Python)
- **Database:** [SQLModel](https://sqlmodel.tiangolo.com/) (ORM) with PostgreSQL
- **RSS Parsing:** `feedparser`
- **Web Crawling:** `Crawl4AI`
- **Entity Extraction:** LLM-based (OpenAI, OpenRouter, or LM Studio)

### Frontend (Planned)
- **Framework:** React 18+ with TypeScript
- **Build Tool:** Vite
- **Styling:** Vanilla CSS with a "Command Center" dark aesthetic.

## 🏁 Getting Started

### Prerequisites
- Python 3.10+
- PostgreSQL

### Backend Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd NewsMonitor
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r backend/requirements.txt
    ```

3.  **Configure environment:**
    Copy `backend/.env.sample` to `backend/.env` and fill in your credentials:
    ```bash
    cp backend/.env.sample backend/.env
    ```
    Ensure `LLM_API_KEY`, `LLM_BASE_URL`, and `DATABASE_URL` are correctly set.

4.  **Initialize Feed Links:**
    Add RSS feed URLs to `links.txt` at the root of the project.

5.  **Run the server:**
    ```bash
    python -m backend.main
    ```
    The API will be available at `http://localhost:8000`.

### API Endpoints

-   `GET /feeds/refresh`: Triggers a fetch of new articles from RSS feeds.
-   `POST /feeds/extract`: Triggers entity extraction and summarization for pending articles.
-   `GET /articles`: Retrieves processed articles and entities.

## 📐 Architecture & Design

Global Pulse follows a modular architecture:
- **`rss_service.py`**: Handles feed ingestion.
- **`crawler_service.py`**: Manages full-text content retrieval.
- **`extraction_service.py`**: Orchestrates LLM interactions for entity mining.
- **`models.py`**: Defines the data schema using SQLModel.

### Design Philosophy
The "Command Center" aesthetic leverages deep nocturnal tones, crisp borders, and subtle glassmorphism to create a high-reliability interface. Visual noise is minimized to ensure critical alerts remain the focal point.

## 📜 Development Conventions

- **Python:** Follow PEP 8. Use explicit type hints.
- **Models:** All database models must be defined in `backend/models.py`.
- **API:** RESTful endpoints in `backend/main.py`.

## 🗺️ Roadmap

See `specs/roadmap.md` for the detailed development plan.

---

*Developed for high-stakes operational environments.*
