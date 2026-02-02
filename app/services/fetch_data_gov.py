import csv
import requests
from io import StringIO

SPONSOR_CSV_URL = ( 
    "https://assets.publishing.service.gov.uk/media/697b386baacd0dc9777b4fa1/2026-01-29_-_Worker_and_Temporary_Worker.csv"
)

def fetch_sponsor_csv(): 
    response = requests.get(SPONSOR_CSV_URL) 
    response.raise_for_status() 
    return response.text

def parse_sponsor_csv(csv_text: str):
    #Remove BOM if present
    csv_text = csv_text.replace("\ufeff", "")
    reader = csv.DictReader(StringIO(csv_text))
    #Normalise Headers
    reader.fieldnames = [h.strip() for h in reader.fieldnames] # type: ignore
    sponsors = []

    for row in reader:
        row = {k.strip(): v.strip() for k, v in row.items()}
        sponsors.append({
            "organisation_name": row["Organisation Name"].strip(),
            "town_city": row.get("Town/City", "").strip(),
            "county": row.get("County", "").strip(),
            "type_rating": row.get("Type & Rating", "").strip(),
            "route": row.get("Route", "").strip()
        })
    return sponsors

def fetch_and_parse_sponsor(): 
    csv_text = fetch_sponsor_csv() 
    return parse_sponsor_csv(csv_text)