
from uuid import uuid4
from sqlmodel import Session, create_engine, SQLModel
from backend.models import Article, Country, GeoName, ArticleReadWithEntities
from backend.main import enrich_article_with_coords

# Use an in-memory SQLite database for testing
engine = create_engine("sqlite://")
SQLModel.metadata.create_all(engine)

def test_enrichment():
    with Session(engine) as session:
        # Setup mock data
        uk = Country(name="United Kingdom", alpha2="GB", alpha3="GBR", latitude=54.0, longitude=-2.0)
        session.add(uk)
        
        london = GeoName(geonameid=1, name="London", country_code="GB", latitude=51.5, longitude=-0.1, population=8000000)
        small_london = GeoName(geonameid=2, name="London", country_code="GB", latitude=10.0, longitude=10.0, population=100)
        session.add(london)
        session.add(small_london)
        
        session.commit()

        # Test 1: Country + City (Highest population)
        art1 = Article(title="Test 1", link="link1", source_url="src1", main_country="United Kingdom", main_city="London")
        enriched1 = enrich_article_with_coords(art1, session)
        print(f"Test 1 (London): lat={enriched1.latitude}, lon={enriched1.longitude}")
        assert enriched1.latitude == 51.5
        assert enriched1.longitude == -0.1

        # Test 2: Country only
        art2 = Article(title="Test 2", link="link2", source_url="src2", main_country="United Kingdom", main_city=None)
        enriched2 = enrich_article_with_coords(art2, session)
        print(f"Test 2 (UK only): lat={enriched2.latitude}, lon={enriched2.longitude}")
        assert enriched2.latitude == 54.0
        assert enriched2.longitude == -2.0

        # Test 3: Unknown country
        art3 = Article(title="Test 3", link="link3", source_url="src3", main_country="Narnia", main_city=None)
        enriched3 = enrich_article_with_coords(art3, session)
        print(f"Test 3 (Unknown): lat={enriched3.latitude}, lon={enriched3.longitude}")
        assert enriched3.latitude is None
        assert enriched3.longitude is None

        # Test 4: City not found (fall back to country)
        art4 = Article(title="Test 4", link="link4", source_url="src4", main_country="United Kingdom", main_city="Atlantis")
        enriched4 = enrich_article_with_coords(art4, session)
        print(f"Test 4 (City not found): lat={enriched4.latitude}, lon={enriched4.longitude}")
        assert enriched4.latitude == 54.0
        assert enriched4.longitude == -2.0

        print("All tests passed!")

if __name__ == "__main__":
    try:
        test_enrichment()
    except Exception as e:
        print(f"Tests failed with error: {e}")
        import traceback
        traceback.print_exc()
