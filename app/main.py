from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_utilities import repeat_every
from app.repositories.database_conn import engine
from app.models import sqlachemy_model
from app.services.save_to_db import SaveToDB
from app.api.v1.sponsors_route import sponsor_router
import logging


# Create the tables in the DB if they don't exist
sqlachemy_model.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mini Sponsors Feed App")

@app.on_event("startup") 
def run_sync_once(): 
    SaveToDB.onetime_sync()
    print("Manual sync done")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s" 
)

logger = logging.getLogger(__name__)

app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"], # or ["https://your-frontend.netlify.app"]
    allow_credentials=True, 
    allow_methods=["*"], 
    allow_headers=["*"]
)

app.include_router(sponsor_router)


@app.on_event("startup")
@repeat_every(seconds=60*60*24, wait_first=True)
def daily_sync():
    logger.info("Starting daily sync job")
    SaveToDB.daily_data_sync()
    print("Daily database refresh done")
    logger.info("Daily database refresh done")

@app.get("/health")
def health_check():
    return {"status": "ok"}



    
