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
- [ ] Create location extraction logic (Countries/Cities).
- [ ] Create event categorization (Conflict, Diplomacy, etc.).
- [x] Store assessments in `extracted_entities` table.
- [ ] API endpoint `/assessment`.

## Phase 3: Visual Intelligence
- [ ] Initialize `frontend` with Vite/React/TS.
- [ ] Design "Deep Space" global CSS theme.
- [ ] Build `FeedList` and `AssessmentPanel` components.

## Phase 4: Full Signal
- [ ] Integrate frontend with backend endpoints.
- [ ] Add real-time "Refresh" capability.
- [ ] Final UI/UX polish.

## Phase 5: Scaling & Production
- [ ] **Implement Distributed Task Queue (Redis/Celery).**
- [ ] **Decouple RSS fetching from article crawling.**
- [ ] **Implement Multi-Worker scaling for Crawl4AI.**
- [ ] **Optimize browser resource management (SemaphoreDispatcher).**
- [ ] Add crawler monitoring and auto-retry logic.
