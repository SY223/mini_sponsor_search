from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from app.repositories.database_conn import get_db
from app.models import sqlachemy_model
from app.services.save_to_db import SaveToDB
from app.services.sponsors_services import SponsorServices




sponsor_router = APIRouter(prefix="/sponsors", tags=["Sponsors"])


@sponsor_router.get("/search")
def search(
    name: str | None = None, 
    city: str | None = None,
    route: str | None = None,
    county: str | None = None,
    rating: str | None = None,
    page: int = 1,
    sort: str | None = None,
    db: Session = Depends(get_db)
    ):
    asearch = SponsorServices.search_a_sponsor(
        name=name, city=city, route=route, county=county, rating=rating, page=page, sort=sort, db=db
    ) # type: ignore
    return asearch
    

@sponsor_router.get("/debug/sponsors")
def debug_sponsors(db: Session = Depends(get_db)):
    return db.query(sqlachemy_model.Sponsor).limit(20).all()

@sponsor_router.get("/routes")
def unique_routes(db: Session = Depends(get_db)):
    return SponsorServices.get_all_unique_routes(db=db)

@sponsor_router.get("/search/by-city-route")
def search_city_and_route(city: str, route: str, page: int = 1, db: Session = Depends(get_db)):
    one_search = SponsorServices.search_by_city_and_route(
        city=city, route=route, page=page, db=db
    )
    return one_search
    
