import csv
import requests
from io import StringIO

SPONSOR_CSV_URL = (
    "https://assets.publishing.service.gov.uk/media/697b386baacd0dc9777b4fa1/2026-01-29_-_Worker_and_Temporary_Worker.csv"
)



def fetch_sponsor_csv():
    response = requests.get(SPONSOR_CSV_URL, timeout=30)
    response.raise_for_status()
    return response.text

def parse_sponsor_csv(csv_text: str):
    reader = csv.DictReader(StringIO(csv_text))
    sponsors = []

    for row in reader:
        sponsors.append({
            "organisation_name": row["OrganisationName"].strip(),
            "town_city": row["Town/City"].strip(),
            "county": row["County"].strip(),
            "type_rating": row["Type & Rating"].strip(),
            "route": row["Route"].strip()
        })

    return sponsors