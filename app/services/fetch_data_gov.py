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
        cleaned = { (k or "").strip(): (v or "").strip() for k, v in row.items() }
        sponsors.append({
            "organisation_name": cleaned.get("Organisation Name", ""),
            "town_city": cleaned.get("Town/City", ""),
            "county": cleaned.get("County", ""),
            "type_rating": cleaned.get("Type & Rating", ""),
            "route": cleaned.get("Route", "")
        })
    return sponsors

def fetch_and_parse_sponsor(): 
    csv_text = fetch_sponsor_csv() 
    return parse_sponsor_csv(csv_text)