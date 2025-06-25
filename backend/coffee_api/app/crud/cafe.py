from typing import Optional

from app.crud.base import CRUDBase
from app.models.cafe import Cafe
from app.schemas.cafe import CafeCreate, CafeUpdate, CafeOut
from geoalchemy2 import functions as func
from geoalchemy2.elements import WKTElement
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.utils.geo import point_from_latlon


class CafeCRUD(CRUDBase[Cafe, CafeCreate, CafeUpdate]):
    def _preprocess_input(
        self, data: dict
    ) -> dict:  # okay yes this should be in a service layer, but its easier this way
        """Convert latitude and longitude to a geospatial point."""
        if "latitude" in data and "longitude" in data:
            data["location"] = point_from_latlon(
                latitude=data["latitude"],
                longitude=data["longitude"],
                srid=4326,
            )
            del data["latitude"]
            del data["longitude"]
        return data

    def get_by_name(self, db: Session, name: str) -> Optional[Cafe]:
        stmt = select(Cafe).where(Cafe.name == name)
        return db.execute(stmt).scalars().first()

    def get_by_string(self, db: Session, search_string: str) -> list[Cafe]:
        stmt = select(Cafe).where(Cafe.name.ilike(f"%{search_string}%"))
        return list(db.execute(stmt).scalars().all())

    def get_by_proximity(
        self, db: Session, user_lat: float, user_lon: float, search_radius: int
    ) -> list[tuple[Cafe, float]]:
        user_point = point_from_latlon(
            latitude=user_lat,
            longitude=user_lon,
            srid=4326,
        )

        distance = func.ST_Distance(Cafe.location, user_point).label("distance")

        stmt = (
            select(Cafe, distance)
            .where(func.ST_DWithin(Cafe.location, user_point, search_radius))
            .order_by(distance)
        )

        cafes = db.execute(stmt).all()

        # Unpack SQLAlchemy Row objects into (Cafe, float) tuples
        return [(row[0], float(row[1])) for row in cafes]


cafe_crud = CafeCRUD(model=Cafe)
