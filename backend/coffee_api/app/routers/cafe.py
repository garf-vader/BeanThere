####### Module Imports

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional


####### Internal Imports

from app.models.cafe import Cafe
#from app.crud.cafe import get_cafe, create_cafe
from app.schemas.cafe import CafeCreate
from app.database import get_db

#######

router = APIRouter()