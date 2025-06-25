####### Module Imports

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional


####### Internal Imports

from app.models.cafe import Cafe
from app.crud.cafe import cafe_crud
from app.schemas.cafe import CafeCreate, CafeUpdate
from app.db.database import get_db
from app.schemas.geo import ProximityQuery
from app.schemas.cafe import CafeOut

#######

router = APIRouter()

@router.get("/cafes/nearby", response_model=list[CafeOut])
def get_nearby_cafes(
    query: ProximityQuery = Depends(), db: Session = Depends(get_db)
):  # uses get and query parameters, should be more scaleable this way
    cafes = cafe_crud.get_by_proximity(
        db,
        user_lat=query.user_lat,
        user_lon=query.user_lon,
        search_radius=query.search_radius,
    )
    return [CafeOut.from_model(cafe) for cafe in cafes]

@router.post("/cafes/")
async def create_cafe_endpoint(
    cafe: CafeCreate,
    db: Session = Depends(get_db),
):
    new_cafe = cafe_crud.create(db, cafe)
    return CafeOut.from_model(new_cafe) # these should be in a service layer, but its easier this way


@router.get("/cafes/id/{cafe_id}")
async def get_cafe_endpoint(cafe_id: int, db: Session = Depends(get_db)):
    cafe = cafe_crud.get(db, cafe_id)
    if cafe is None:
        raise HTTPException(status_code=404, detail="cafe not found")
    return CafeOut.from_model(cafe)


@router.put("/cafes/id/{cafe_id}")
async def update_cafe_endpoint(
    cafe_id: int, cafe_update: CafeUpdate, db: Session = Depends(get_db)
):

    db_cafe = cafe_crud.get(db, cafe_id)
    cafe_updated = cafe_crud.update(db, db_cafe, cafe_update)

    return CafeOut.from_model(cafe_updated)


@router.delete("/cafes/id/{cafe_id}")
async def delete_cafe_endpoint(cafe_id: int, db: Session = Depends(get_db)):
    cafe_crud.delete_by_id(db, cafe_id)

    return {"detail": "cafe deleted"}

