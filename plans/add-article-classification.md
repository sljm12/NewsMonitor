# Plan: Add Article Classification

## Objective
Implement a single-category classification system for news articles using a predefined, easily updateable list of topics.

## Key Files & Context
- `specs/roadmap.md`: Update to reflect current progress.
- `backend/config.py`: New file to store the list of categories.
- `backend/models.py`: Update `Article` and `ArticleReadWithEntities` models to include the classification field.
- `backend/extraction_service.py`: Update LLM prompt and processing logic to handle classification.

## Implementation Steps

### 0. Update Roadmap
- Update `specs/roadmap.md` to mark "Create event categorization" as in-progress or completed once done.

### 1. Create Configuration File
- Create `backend/config.py` with a list of initial categories.
```python
ARTICLE_CATEGORIES = [
    "Geopolitics",
    "Economics",
    "Conflict/War",
    "Technology",
    "Environment",
    "Diplomacy",
    "Internal Politics",
    "Human Rights",
    "Health",
    "Culture"
]
```

### 2. Update Database Models
- In `backend/models.py`:
    - Add `classification: Optional[str] = Field(default=None, index=True)` to the `Article` class.
    - Add `classification: Optional[str] = None` to the `ArticleReadWithEntities` class.

### 3. Update Extraction Service
- In `backend/extraction_service.py`:
    - Import `ARTICLE_CATEGORIES` from `backend.config`.
    - Update `SYSTEM_PROMPT` to:
        - Include the list of available categories.
        - Instruct the LLM to choose exactly one category from the list.
        - Add `classification` to the expected JSON response.
    - Update `analyze_article_content` to extract the `classification` from the LLM response.
    - Update `process_unassessed_articles` to save the `classification` to the `Article` instance.

### 4. Verification & Testing
- Run `backend/extraction_service.py` directly to verify it processes unassessed articles and assigns a classification.
- Check the database (or API response) to ensure the classification is correctly stored.

### 5. Finalize Documentation
- Save this plan to `plans/add-article-classification.md` in the project root.
