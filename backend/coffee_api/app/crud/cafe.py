from typing import Optional

from app.models.cafe import Cafe
from app.schemas.cafe import CafeCreate, CafeUpdate
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase

# Uncomment class to override CRUD or add model-specific functions
#class CafeCRUD(CRUDBase[CafeReview, CafeCreate, CafeUpdate]):

cafe_crud = CRUDBase(model=Cafe)