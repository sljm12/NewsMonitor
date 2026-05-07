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
    main_country: Optional[str] = Field(default=None, index=True)
    main_city: Optional[str] = Field(default=None, index=True)
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

class Country(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    alpha2: str = Field(unique=True, index=True)
    alpha3: str = Field(unique=True, index=True)
    numeric_code: Optional[int] = None
    latitude: float
    longitude: float

class GeoName(SQLModel, table=True):
    __tablename__ = "geonames"
    geonameid: int = Field(primary_key=True)
    name: Optional[str] = Field(default=None, index=True)
    asciiname: Optional[str] = None
    alternatenames: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    feature_class: Optional[str] = None
    feature_code: Optional[str] = None
    country_code: Optional[str] = Field(default=None, index=True)
    cc2: Optional[str] = None
    admin1_code: Optional[str] = None
    admin2_code: Optional[str] = None
    admin3_code: Optional[str] = None
    admin4_code: Optional[str] = None
    population: Optional[int] = None
    elevation: Optional[int] = None
    dem: Optional[int] = None
    timezone: Optional[str] = None
    modification_date: Optional[datetime] = None

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
    main_country: Optional[str] = None
    main_city: Optional[str] = None
    published_at: Optional[datetime] = None
    source_url: str
    created_at: datetime
    assessment_done: bool
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    entities: List[ExtractedEntityRead] = []
