from fastapi import Depends, status, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import sqlachemy_model
from app.repositories.database_conn import get_db
from datetime import datetime

class SponsorServices():
    @staticmethod
    def search_a_sponsor(
        name: str | None = None, 
        city: str | None = None,
        route: str | None = None,
        county: str | None = None,
        rating: str | None = None,
        page: int = 1,
        sort: str | None = None,
        db: Session = Depends(get_db)
        ):
        page_size = 20
        offset = (page - 1) * page_size
        #Base Query
        query = db.query(sqlachemy_model.Sponsor)
        #fliter by company name
        if name:
            query = query.filter(
                func.lower(sqlachemy_model.Sponsor.organisation_name)
                .contains(name.lower().strip()))
        #Optional filter by town/city
        if city:
            query = query.filter(
                func.lower(sqlachemy_model.Sponsor.town_city)
                .contains(city.lower().strip()))
        if route:
            query = query.filter(func.lower(sqlachemy_model.Sponsor.route) == route.lower().strip())
        if county:
            query = query.filter(func.lower(sqlachemy_model.Sponsor.county).contains(county.lower().strip()))
        if rating:
            query = query.filter(func.lower(sqlachemy_model.Sponsor.type_rating) == rating.lower().strip())
        if sort == "asc":
            query = query.order_by(sqlachemy_model.Sponsor.organisation_name.asc())
        if sort == "desc":
            query = query.order_by(sqlachemy_model.Sponsor.organisation_name.desc())
        #total count before pagination
        total_results = query.count() # type: ignore
        if not query:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The company provided is not on the list.")
        if total_results == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="The company provided is not on the list"
            )
        #paginated results
        results = (query.offset(offset).limit(page_size).all())
        return {
            "message": f"Search successful with {total_results} results",
            "page": page,
            "page_size": page_size,
            "total_results": total_results,
            "total_pages": (total_results + page_size -1) // page_size,
            "data": results
        }
    
    @staticmethod
    def get_all_unique_routes(db: Session = Depends(get_db)):
        routes = (
            db.query(sqlachemy_model.Sponsor.route).distinct()
            .order_by(sqlachemy_model.Sponsor.route.asc())
            .all()
        )
        unique_routes = [r[0] for r in routes]
        return {
            "count": len(unique_routes),
            "routes": unique_routes
        }
    
    @staticmethod
    def search_by_city_and_route(city: str, route: str, page: int = 1, db: Session = Depends(get_db)):
        page_size = 20
        offset = (page - 1) * page_size

        query = db.query(sqlachemy_model.Sponsor).filter(
            func.lower(sqlachemy_model.Sponsor.town_city) == city.lower().strip(),
            func.lower(sqlachemy_model.Sponsor.route) == route.lower().strip()
        )

        total_results = query.count()
        if total_results == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No sponsors found for this city and route")
        
        results = (query.offset(offset).limit(page_size).all())
        return {
            "message": "Search successful",
            "city": city,
            "route": route,
            "page": page,
            "page_size": page_size,
            "total_results": total_results,
            "total_pages": (total_results + page_size),
            "data": results
        }

    @staticmethod
    def get_revoked_sponsors(
        db: Session = Depends(get_db),
        page: int = 1
        ):
        page_size = 20
        offset = (page - 1) * 20
        revoked_licences = (
            db.query(sqlachemy_model.RemovedSponsor).order_by(sqlachemy_model.RemovedSponsor.removed_on.desc())
        )
        total_results = revoked_licences.count() # type: ignore
        if total_results == 0:
            return {"message": "No sponsor licence revoked"}
        results = (
            revoked_licences.offset(offset).limit(page_size).all() # type: ignore
        )
        return {
            "message": "Revoked sponsors retrieved successfully",
            "page": page,
            "page_size": page_size,
            "total_results": total_results,
            "total_pages": (total_results + page_size - 1) // page_size,
            "data": results
        }