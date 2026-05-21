# Roadmap: Global Pulse Implementation

## Phase 1: Foundation & Data Acquisition
- [x] Initialize `backend` directory with FastAPI & SQLAlchemy.
- [x] Setup PostgreSQL connection (SQLModel for ORM).
- [x] Implement RSS service to fetch items from `links.txt`.
- [x] Implement DB persistence (Unique link constraint for upserts).
- [x] Integrate Crawl4AI for browser-based article scraping.
- [x] Store full article markdown in the database.
- [x] Basic API endpoint `/feeds` (serving from DB).

## Phase 2: Intelligence Layer
- [x] **Implement LLM-powered summarization using full article text.**
- [x] Create location extraction logic (Countries/Cities).
- [/] Create event categorization (Conflict, Diplomacy, etc.) [IN PROGRESS]
  - [x] Implement single-category classification using a predefined list.
- [x] Store assessments in `extracted_entities` table.
- [x] API endpoint `/assessment`.
- [x] Implement structured API response returning articles with nested extracted entities.

## Phase 3: Narrative Synthesis & Event Clustering
- [x] **Implement Automated Event Identification.**
  - [x] Update `extraction_service.py` to identify canonical event names (e.g., "2026 G7 Summit").
  - [/] Integrate vector similarity search to group similar articles semantically. [PLANNED]
- [x] **Automatic Article-to-Event Tagging.**
  - [x] Link `Article` records to a central `Event` record upon ingestion.
  - [ ] Enable "Event Overview" views by aggregating tagged articles.
- [ ] **Event & Entity Wiki Pages.**
  - [ ] Generate summarized "Wiki" content for Events and key People/Organizations.
  - [ ] Implement automated **Timeline Generation** based on aggregated article dates and key developments.

## Phase 4: Visual Intelligence
- [ ] Initialize `frontend` with Vite/React/TS.
- [ ] Design "Deep Space" global CSS theme.
- [ ] Build `FeedList` and `AssessmentPanel` components.

## Phase 5: Full Signal
- [ ] Integrate frontend with backend endpoints.
- [ ] Add real-time "Refresh" capability.
- [ ] Final UI/UX polish.

## Phase 6: Scaling & Production
- [ ] **Implement Distributed Task Queue (Redis/Celery).**
- [ ] **Decouple RSS fetching from article crawling.**
- [ ] **Implement Multi-Worker scaling for Crawl4AI.**
- [ ] **Optimize browser resource management (SemaphoreDispatcher).**
- [ ] Add crawler monitoring and auto-retry logic.
