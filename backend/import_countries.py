import csv
import os
from sqlmodel import Session, select
from backend.database import engine, init_db
from backend.models import Country

def import_countries(csv_file_path: str):
    """Imports country data from a CSV file into the database."""
    if not os.path.exists(csv_file_path):
        print(f"Error: CSV file not found at {csv_file_path}")
        return

    # Ensure the table is created
    init_db()

    with Session(engine) as session:
        from backend.migrate_country_areas import MAPPING
        with open(csv_file_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            count = 0
            for row in reader:
                alpha2 = row.get('Alpha-2 code') or row.get('alpha2')
                if not alpha2:
                    continue
                
                # Check if country already exists
                existing = session.exec(select(Country).where(Country.alpha2 == alpha2)).first()
                if existing:
                    # Update area if not set
                    area = MAPPING.get(alpha2)
                    if area and not existing.area:
                        existing.area = area
                        session.add(existing)
                        count += 1
                    continue

                name = row.get('Country') or row.get('name')
                alpha3 = row.get('Alpha-3 code') or row.get('alpha3')
                numeric_code_str = row.get('Numeric code') or row.get('numeric_code')
                latitude_str = row.get('Latitude (average)') or row.get('latitude')
                longitude_str = row.get('Longitude (average)') or row.get('longitude')

                try:
                    country = Country(
                        name=name,
                        alpha2=alpha2,
                        alpha3=alpha3,
                        numeric_code=int(numeric_code_str) if numeric_code_str else None,
                        latitude=float(latitude_str) if latitude_str else 0.0,
                        longitude=float(longitude_str) if longitude_str else 0.0,
                        area=MAPPING.get(alpha2)
                    )
                    session.add(country)
                    count += 1
                except ValueError as e:
                    print(f"Skipping row due to error: {row}. Error: {e}")

            session.commit()
            print(f"Imported/Updated {count} countries.")

if __name__ == "__main__":
    csv_path = os.path.join(os.getcwd(), "country.csv")
    import_countries(csv_path)
