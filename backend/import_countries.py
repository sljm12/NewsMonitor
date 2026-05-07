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
        with open(csv_file_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            count = 0
            for row in reader:
                alpha2 = row['Alpha-2 code']
                
                # Check if country already exists
                existing = session.exec(select(Country).where(Country.alpha2 == alpha2)).first()
                if existing:
                    continue

                try:
                    country = Country(
                        name=row['Country'],
                        alpha2=alpha2,
                        alpha3=row['Alpha-3 code'],
                        numeric_code=int(row['Numeric code']) if row['Numeric code'] else None,
                        latitude=float(row['Latitude (average)']),
                        longitude=float(row['Longitude (average)'])
                    )
                    session.add(country)
                    count += 1
                except ValueError as e:
                    print(f"Skipping row due to error: {row}. Error: {e}")

            session.commit()
            print(f"Imported {count} new countries.")

if __name__ == "__main__":
    csv_path = os.path.join(os.getcwd(), "country.csv")
    import_countries(csv_path)
