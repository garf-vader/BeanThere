####### Module Imports

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional


####### Internal Imports

from app.models.user import User
#from app.crud.user import get_user, create_user
from app.schemas.user import UserCreate
from app.db.database import get_db

#######

router = APIRouter()