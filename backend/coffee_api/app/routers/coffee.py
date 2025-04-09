####### Module Imports

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional


####### Internal Imports

from app.models.coffee import CoffeeReview
from app.crud.coffee import get_review, create_review
from app.schemas.coffee import CoffeeReviewCreate
from app.database import get_db

#######

router = APIRouter()

@router.post("/reviews/")
async def create_review_endpoint(
    review: CoffeeReviewCreate,
    db: Session = Depends(get_db),
):
    return create_review(db, review)


@router.get("/reviews/{review_id}")
async def get_review_endpoint(review_id: int, db: Session = Depends(get_db)):
    review = get_review(db, review_id)
    if review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    return review


@router.put("/reviews/{review_id}")
async def update_review_endpoint(
    review_id: int,
    drinkType: str,
    roastDarkness: int,
    tasteRating: int,
    price: float,
    notes: Optional[str] = None,
    db: Session = Depends(get_db),
):
    review = db.query(CoffeeReview).filter(CoffeeReview.id == review_id).first()
    if review is None:
        raise HTTPException(status_code=404, detail="Review not found")

    review.drinkType = drinkType
    review.roastDarkness = roastDarkness
    review.tasteRating = tasteRating
    review.price = price
    review.notes = notes
    db.commit()
    db.refresh(review)

    return review


@router.delete("/reviews/{review_id}")
async def delete_review_endpoint(review_id: int, db: Session = Depends(get_db)):
    review = db.query(CoffeeReview).filter(CoffeeReview.id == review_id).first()
    if review is None:
        raise HTTPException(status_code=404, detail="Review not found")

    db.delete(review)
    db.commit()

    return {"detail": "Review deleted"}