from pydantic import BaseModel
from typing import Optional

# Pydantic model for Cafe
class CafeCreate(BaseModel):
    name: str
    location: Optional[str] = None

    class Config:
        from_attributes = True  # Allows Pydantic to work with SQLAlchemy models

# Pydantic model for CoffeeReview
class CoffeeReviewCreate(BaseModel):
    drinkType: str
    roastDarkness: Optional[int] = None
    tasteRating: Optional[int] = None
    price: Optional[float] = None
    notes: Optional[str] = None
    cafeId: Optional[int] = None  # ID of the related cafe

    class Config:
        from_attributes = True  # Allows Pydantic to work with SQLAlchemy models
