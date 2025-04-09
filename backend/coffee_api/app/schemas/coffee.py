from pydantic import BaseModel
from typing import Optional

# Pydantic model for CoffeeReview
class CoffeeReviewCreate(BaseModel):
    drinkType: str
    roastDarkness: Optional[int] = None
    tasteRating: Optional[int] = None
    price: Optional[float] = None
    notes: Optional[str] = None
    cafeId: Optional[int] = None  # ID of the related cafe
    userId: Optional[int] = None # ID of the user submitting the review

    class Config:
        from_attributes = True  # Allows Pydantic to work with SQLAlchemy models