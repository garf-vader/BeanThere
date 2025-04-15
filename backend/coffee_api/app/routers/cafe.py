####### Module Imports

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional


####### Internal Imports

from app.models.cafe import Cafe
from app.crud.cafe import cafe_crud
from app.schemas.cafe import CafeCreate, CafeUpdate
from app.db.database import get_db

#######

router = APIRouter()


@router.post("/cafes/")
async def create_cafe_endpoint(
    cafe: CafeCreate,
    db: Session = Depends(get_db),
):
    return cafe_crud.create(db, cafe)


@router.get("/cafes/{cafe_id}")
async def get_cafe_endpoint(cafe_id: int, db: Session = Depends(get_db)):
    cafe = cafe_crud.get(db, cafe_id)
    if cafe is None:
        raise HTTPException(status_code=404, detail="cafe not found")
    return cafe


@router.put("/cafes/{cafe_id}")
async def update_cafe_endpoint(
    cafe: CafeUpdate,
    db: Session = Depends(get_db)
):
    cafe_crud.update(db, cafe)

    return cafe


@router.delete("/cafes/{cafe_id}")
async def delete_cafe_endpoint(cafe_id: int, db: Session = Depends(get_db)):
    cafe_crud.delete_by_id(db, cafe_id)

    return {"detail": "cafe deleted"}
