from sqlalchemy.orm import Session
from app.models.sqlachemy_model import Sponsor, RemovedSponsor
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
        incoming_records = {}
        for r in records:
            r = SaveToDB.normalise_record(r)
            key = (r["organisation_name"], r["route"])
            incoming_records[key] = r
        #Load existing sponsors
        existing_records = {
            (s.organisation_name, s.route): s for s in db.query(Sponsor).all()
        }
        # 3. Compute diff 
        existing_keys = set(existing_records.keys())
        incoming_keys = set(incoming_records.keys())

        removed_keys = existing_keys - incoming_keys
        new_keys = incoming_keys - existing_keys
        common_keys = existing_keys & incoming_keys

        removed_count = len(removed_keys)
        print(removed_count, "sponsor licence revoked")
        #Store Removed Keys to database
        for key in removed_keys:
            old = existing_records[key]
            # Check if already stored 
            exists = db.query(RemovedSponsor).filter_by( organisation_name=old.organisation_name, route=old.route ).first()
            if exists:
                continue
            removed_entry = RemovedSponsor(
                organisation_name = old.organisation_name,
                route = old.route,
                removed_on = datetime.utcnow()
            )
            db.add(removed_entry)
        
        #Add new companies
        for key in new_keys:
            db.add(Sponsor(**incoming_records[key]))

        for key in common_keys:
            obj = existing_records[key]
            data = incoming_records[key]
            obj.town_city = data["town_city"]
            obj.county = data["county"]
            obj.type_rating = data["type_rating"]
            obj.last_synced = datetime.utcnow()
        
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



