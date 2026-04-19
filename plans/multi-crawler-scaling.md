# Plan: Multi-Crawler Scaling Architecture

## Background & Motivation
As the number of RSS feeds and articles grows, a single-threaded or even a simple async loop will become a bottleneck. Article crawling (Crawl4AI) is I/O and CPU bound due to browser overhead. Scaling requires a distributed architecture that can handle spikes in volume and provide resilience.

## Scope & Impact
- **Affected Components:** `backend/rss_service.py` (producer), New `backend/worker.py` (consumer), `backend/models.py` (tracking status).
- **Impact:** Significant increase in throughput; decoupling of discovery and extraction; improved error handling and retries.

## Proposed Solution
Transition from a monolithic service to a **Distributed Task Queue** architecture.

### 1. Infrastructure
- **Message Broker:** Redis for task management.
- **Task Runner:** Celery or `arq` (async-first).
- **Concurrency:** `SemaphoreDispatcher` within Crawl4AI to manage local browser resources.

### 2. Implementation Strategy
- **Task Definition:** Create a `crawl_article` task that takes an `article_id`.
- **Producer Logic:** `rss_service` will enqueue `crawl_article` tasks after storing the basic RSS metadata.
- **Worker Logic:** Workers will run `AsyncWebCrawler.arun()` (or `arun_many` for batches), update the DB with `full_text`, and mark the article as ready for LLM processing.

## Phased Implementation Plan

### Phase 1: Task Queue Integration
- [ ] Add `redis` and `celery` (or `arq`) to `requirements.txt`.
- [ ] Implement `backend/tasks.py` for task definitions.
- [ ] Update `rss_service.py` to trigger tasks instead of direct crawling.

### Phase 2: Crawler Worker
- [ ] Implement `backend/worker.py` with optimized Crawl4AI configuration (BrowserConfig, RunConfig).
- [ ] Implement batching logic using `arun_many` to maximize throughput per browser instance.

### Phase 3: Monitoring & Resilience
- [ ] Implement retry logic for failed crawls (e.g., timeouts, 403 Forbidden).
- [ ] Add basic monitoring (queue depth, worker health).

## Documentation Updates

### `specs/roadmap.md`
Add the following to the end of the file:
```markdown
## Phase 5: Scaling & Production
- [ ] **Implement Distributed Task Queue (Redis/Celery).**
- [ ] **Decouple RSS fetching from article crawling.**
- [ ] **Implement Multi-Worker scaling for Crawl4AI.**
- [ ] **Optimize browser resource management (SemaphoreDispatcher).**
- [ ] Add crawler monitoring and auto-retry logic.
```

### `GEMINI.md`
Update the **Architecture** section to include:
```markdown
### Future Scaling (Planned)
- **Task Queue:** Redis/Celery for distributed processing.
- **Distributed Crawling:** Decoupled workers running Crawl4AI to handle high-volume ingestions.
```

## Verification & Testing
- **Local Integration:** Run Redis locally and verify workers pick up tasks.
- **Stress Test:** Feed 100+ articles simultaneously and monitor worker resource usage.
- **Resilience:** Kill a worker during a crawl and ensure the task is retried.
