####### Module Imports

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional


####### Internal Imports

from app.models.coffee import CoffeeReview
from app.crud.coffee import coffee_crud
from app.schemas.coffee import CoffeeReviewCreate, CoffeeReviewUpdate
from app.db.database import get_db

#######

router = APIRouter()


@router.post("/reviews/")
async def create_review_endpoint(
    review: CoffeeReviewCreate,
    db: Session = Depends(get_db),
):
    return coffee_crud.create(db, review)


@router.get("/reviews/{review_id}")
async def get_review_endpoint(review_id: int, db: Session = Depends(get_db)):
    review = coffee_crud.get(db, review_id)
    if review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    return review


@router.put("/reviews/{review_id}")
async def update_review_endpoint(
    review: CoffeeReviewUpdate,
    db: Session = Depends(get_db)
):
    coffee_crud.update(db, review)

    return review


@router.delete("/reviews/{review_id}")
async def delete_review_endpoint(review_id: int, db: Session = Depends(get_db)):
    coffee_crud.delete_by_id(db, review_id)

    return {"detail": "Review deleted"}
