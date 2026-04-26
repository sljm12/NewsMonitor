from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4
from sqlmodel import Field, Relationship, SQLModel

class Article(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    title: str
    link: str = Field(unique=True, index=True)
    rss_summary: Optional[str] = None
    full_text: Optional[str] = None
    summary: Optional[str] = None
    classification: Optional[str] = Field(default=None, index=True)
    published_at: Optional[datetime] = None
    source_url: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    assessment_done: bool = Field(default=False)

    entities: List["ExtractedEntity"] = Relationship(back_populates="article")

class ExtractedEntity(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    article_id: UUID = Field(foreign_key="article.id")
    entity_name: str
    entity_type: str  # e.g., "Location", "Organization", "Event"
    confidence: float = Field(default=1.0)

    article: Article = Relationship(back_populates="entities")

class ExtractedEntityRead(SQLModel):
    id: UUID
    entity_name: str
    entity_type: str
    confidence: float

class ArticleReadWithEntities(SQLModel):
    id: UUID
    title: str
    link: str
    rss_summary: Optional[str] = None
    full_text: Optional[str] = None
    summary: Optional[str] = None
    classification: Optional[str] = None
    published_at: Optional[datetime] = None
    source_url: str
    created_at: datetime
    assessment_done: bool
    entities: List[ExtractedEntityRead] = []
