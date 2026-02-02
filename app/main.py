from fastapi import FastAPI
from fastapi_utilities import repeat_every
from app.repositories.database_conn import engine
from app.models import sqlachemy_model
from app.services.save_to_db import SaveToDB
from app.api.v1.sponsors_route import sponsor_router


# Create the tables in the DB if they don't exist
sqlachemy_model.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mini Sponsors Feed App")

# @app.on_event("startup") 
# def run_sync_once(): 
#     SaveToDB.onetime_sync()
#     print("Manual sync done")

@app.on_event("startup")
@repeat_every(seconds=60*60*24, wait_first=True)
def daily_sync():
    SaveToDB.daily_data_sync()
    print("Daily database refresh done")

app.include_router(sponsor_router)



    
