from typing import Optional

from app.models.coffee import CoffeeReview
from app.schemas.coffee import CoffeeReviewCreate
from sqlalchemy.orm import Session


def get_review(db: Session, review_id: int):
    return db.query(CoffeeReview).filter(CoffeeReview.id == review_id).first()


def create_review(db: Session, review: CoffeeReviewCreate) -> CoffeeReview:
    # Creates a new coffee review in the database
    db_review = CoffeeReview(
        drinkType=review.drinkType,
        roastDarkness=review.roastDarkness,
        tasteRating=review.tasteRating,
        price=review.price,
        notes=review.notes,
        cafeId=review.cafeId,  # Currently an Integer Reference to Cafe DB, might instead assign each cafe a unique code
        userId=review.userId # Currently an Integer Reference to Cafe DB, might instead assign each user a unique code
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review
