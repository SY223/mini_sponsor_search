from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint, Index, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import validates
from datetime import datetime



Base = declarative_base()

class Sponsor(Base):
    __tablename__="sponsors"

    id = Column(Integer, primary_key=True, index=True)
    organisation_name = Column(Text, nullable=False)
    town_city = Column(Text)
    county = Column(Text)
    type_rating = Column(Text)
    route = Column(Text)
    last_updated = Column(DateTime, default=datetime.utcnow)

    # Prevent duplicate rows for the same company on the same route
    __table_args__ = (
        UniqueConstraint('organisation_name', 'route', name='uq_org_route'),
    )
    @validates("organisation_name", "town_city", "county", "type_rating", "route") 
    def convert_lower(self, key, value): 
        return value.lower() if isinstance(value, str) else value
  
