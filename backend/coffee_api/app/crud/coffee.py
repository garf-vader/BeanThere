from typing import Optional

from app.models.coffee import CoffeeReview
from app.schemas.coffee import CoffeeReviewCreate, CoffeeReviewUpdate
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase

# Uncomment class to override CRUD or add model-specific functions
#class CoffeeCRUD(CRUDBase[CoffeeReview, CoffeeReviewCreate, CoffeeReviewUpdate]):

coffee_crud = CRUDBase(model=CoffeeReview)