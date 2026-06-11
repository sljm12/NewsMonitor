import os
from sqlalchemy import text
from sqlmodel import Session, select
from backend.database import engine
from backend.models import Country
from dotenv import load_dotenv

load_dotenv(dotenv_path="backend/.env")

# Country classification mapping (244 countries mapped)
MAPPING = {
    "US": "North America", "CA": "North America", "MX": "North America",
    "BM": "North America", "PM": "North America", "GL": "North America",

    "CN": "East Asia", "JP": "East Asia", "KP": "East Asia", "KR": "East Asia",
    "TW": "East Asia", "MN": "East Asia", "HK": "East Asia", "MO": "East Asia",

    "ID": "Southeast Asia", "PH": "Southeast Asia", "VN": "Southeast Asia",
    "TH": "Southeast Asia", "MY": "Southeast Asia", "SG": "Southeast Asia",
    "MM": "Southeast Asia", "KH": "Southeast Asia", "LA": "Southeast Asia",
    "BN": "Southeast Asia", "TL": "Southeast Asia",

    "KZ": "Central Asia", "UZ": "Central Asia", "TM": "Central Asia",
    "KG": "Central Asia", "TJ": "Central Asia",

    "IN": "South Asia", "PK": "South Asia", "BD": "South Asia", "AF": "South Asia",
    "LK": "South Asia", "NP": "South Asia", "BT": "South Asia", "MV": "South Asia",

    "RU": "Russia & Eurasia (Post-Soviet Space)",
    "UA": "Russia & Eurasia (Post-Soviet Space)",
    "BY": "Russia & Eurasia (Post-Soviet Space)",
    "MD": "Russia & Eurasia (Post-Soviet Space)",
    "GE": "Russia & Eurasia (Post-Soviet Space)",
    "AM": "Russia & Eurasia (Post-Soviet Space)",
    "AZ": "Russia & Eurasia (Post-Soviet Space)",

    "DZ": "Middle East & North Africa (MENA)",
    "BH": "Middle East & North Africa (MENA)",
    "EG": "Middle East & North Africa (MENA)",
    "IR": "Middle East & North Africa (MENA)",
    "IQ": "Middle East & North Africa (MENA)",
    "IL": "Middle East & North Africa (MENA)",
    "JO": "Middle East & North Africa (MENA)",
    "KW": "Middle East & North Africa (MENA)",
    "LB": "Middle East & North Africa (MENA)",
    "LY": "Middle East & North Africa (MENA)",
    "MA": "Middle East & North Africa (MENA)",
    "OM": "Middle East & North Africa (MENA)",
    "PS": "Middle East & North Africa (MENA)",
    "QA": "Middle East & North Africa (MENA)",
    "SA": "Middle East & North Africa (MENA)",
    "SY": "Middle East & North Africa (MENA)",
    "TN": "Middle East & North Africa (MENA)",
    "TR": "Middle East & North Africa (MENA)",
    "AE": "Middle East & North Africa (MENA)",
    "YE": "Middle East & North Africa (MENA)",
    "EH": "Middle East & North Africa (MENA)",
    "CY": "Middle East & North Africa (MENA)",

    "AU": "Oceania & the Pacific", "NZ": "Oceania & the Pacific",
    "FJ": "Oceania & the Pacific", "PG": "Oceania & the Pacific",
    "SB": "Oceania & the Pacific", "VU": "Oceania & the Pacific",
    "WS": "Oceania & the Pacific", "KI": "Oceania & the Pacific",
    "TO": "Oceania & the Pacific", "FM": "Oceania & the Pacific",
    "MH": "Oceania & the Pacific", "PW": "Oceania & the Pacific",
    "TV": "Oceania & the Pacific", "NR": "Oceania & the Pacific",
    "NC": "Oceania & the Pacific", "PF": "Oceania & the Pacific",
    "GU": "Oceania & the Pacific", "MP": "Oceania & the Pacific",
    "AS": "Oceania & the Pacific", "CK": "Oceania & the Pacific",
    "NU": "Oceania & the Pacific", "TK": "Oceania & the Pacific",
    "WF": "Oceania & the Pacific", "PN": "Oceania & the Pacific",
    "UM": "Oceania & the Pacific", "NF": "Oceania & the Pacific",
    "CC": "Oceania & the Pacific", "CX": "Oceania & the Pacific",
    "AI": "Latin America & the Caribbean",
    "IO": "Sub-Saharan Africa",
}

# Add Europe
EUROPE_CODES = {
    "AL", "AD", "AT", "BE", "BA", "BG", "HR", "CZ", "DK", "EE", "FI", "FR", "DE", "GR", "HU", "IS", "IE", "IT",
    "LV", "LI", "LT", "LU", "MT", "MC", "ME", "NL", "MK", "NO", "PL", "PT", "RO", "SM", "RS", "SK", "SI", "ES",
    "SE", "CH", "GB", "VA", "AX", "FO", "GI", "GG", "IM", "JE", "SJ"
}
for code in EUROPE_CODES:
    MAPPING[code] = "Europe"

# Add Sub-Saharan Africa
SSA_CODES = {
    "AO", "BJ", "BW", "BF", "BI", "CM", "CV", "CF", "TD", "KM", "CG", "CD", "CI", "DJ", "GQ", "ER", "SZ", "ET",
    "GA", "GM", "GH", "GN", "GW", "KE", "LS", "LR", "MG", "MW", "ML", "MR", "MU", "MZ", "NA", "NE", "NG", "RW",
    "ST", "SN", "SC", "SL", "SO", "ZA", "SS", "SD", "TZ", "TG", "UG", "ZM", "ZW", "YT", "RE", "SH"
}
for code in SSA_CODES:
    MAPPING[code] = "Sub-Saharan Africa"

# Add Latin America & the Caribbean
LAC_CODES = {
    "AR", "BO", "BR", "CL", "CO", "EC", "FK", "GF", "GY", "PY", "PE", "SR", "UY", "VE",
    "BS", "BB", "CU", "DM", "DO", "GD", "HT", "JM", "KN", "LC", "VC", "TT", "AG", "BZ",
    "CR", "SV", "GT", "HN", "NI", "PA", "AW", "VG", "KY", "GP", "MQ", "MS", "AN", "PR",
    "BL", "MF", "TC", "VI", "SX", "BQ", "CW"
}
for code in LAC_CODES:
    MAPPING[code] = "Latin America & the Caribbean"

# Antarctic/other
MAPPING["AQ"] = "Oceania & the Pacific"
MAPPING["BV"] = "Europe"
MAPPING["GS"] = "Latin America & the Caribbean"
MAPPING["HM"] = "Oceania & the Pacific"
MAPPING["TF"] = "Sub-Saharan Africa"

def migrate():
    """Adds area column to country table and populates it."""
    with engine.connect() as connection:
        print("Starting migration: Adding area column to 'country' table...")
        try:
            # Check if area already exists
            check_sql = text("SELECT column_name FROM information_schema.columns WHERE table_name='country' AND column_name='area';")
            result = connection.execute(check_sql).fetchone()
            
            if not result:
                connection.execute(text("ALTER TABLE country ADD COLUMN area VARCHAR;"))
                connection.execute(text("CREATE INDEX ix_country_area ON country (area);"))
                print("Added column 'area' and its index.")
            else:
                print("Column 'area' already exists.")
            connection.commit()
        except Exception as e:
            print(f"Error adding column: {e}")
            connection.rollback()
            return

    # Populate country areas
    with Session(engine) as session:
        countries = session.exec(select(Country)).all()
        updated_count = 0
        for country in countries:
            area = MAPPING.get(country.alpha2)
            if area and country.area != area:
                country.area = area
                session.add(country)
                updated_count += 1
        
        session.commit()
        print(f"Migration completed. Updated {updated_count} countries.")

if __name__ == "__main__":
    migrate()
