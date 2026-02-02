from sqlalchemy.orm import Session
from app.models.sqlachemy_model import Sponsor
from app.repositories.database_conn import SessionLocal
from app.services import fetch_data_gov
from datetime import datetime



class SaveToDB():
    @staticmethod
    def normalise_record(record: dict) -> dict: 
        return {
            "organisation_name": record["organisation_name"].lower(), 
            "town_city": record["town_city"].lower() if record["town_city"] else "", 
            "county": record["county"].lower() if record["county"] else "", 
            "type_rating": record["type_rating"].lower() if record["type_rating"] else "", 
            "route": record["route"].lower(), "last_updated": record.get("last_updated")
        }

    @staticmethod
    def sync_data_to_db(db: Session, records: list):
        #Deduplicate incoming records
        unique_records = {}
        for r in records:
            r = SaveToDB.normalise_record(r)
            key = (r["organisation_name"], r["route"])
            unique_records[key] = r
        #Load existing sponsors
        existing_records = {
            (s.organisation_name, s.route): s for s in db.query(Sponsor).all()
        }
        for key, record in unique_records.items():
            if key in existing_records:
                obj = existing_records[key]
                obj.town_city = record["town_city"]
                obj.county = record["county"]
                obj.type_rating = record["type_rating"]
                obj.last_synced = datetime.utcnow()
            else:
                new_sponsor = Sponsor(**record)
                db.add(new_sponsor)
        
        db.commit()

    @staticmethod
    def onetime_sync():
        db = SessionLocal() 
        raw = fetch_data_gov.fetch_and_parse_sponsor()
        results = SaveToDB.sync_data_to_db(db, raw)
        db.close()
        return results
    
    @staticmethod
    def daily_data_sync():
        db = SessionLocal()
        try:
            raw_data = fetch_data_gov.fetch_and_parse_sponsor()
            SaveToDB.sync_data_to_db(db, raw_data)
            print("sync successful")
        finally:
            db.close()



