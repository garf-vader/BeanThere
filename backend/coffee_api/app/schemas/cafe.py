from typing import Optional

from pydantic import BaseModel


# Pydantic model for Cafe
class CafeCreate(BaseModel):
    name: str
    location: Optional[str] = None

    class Config:
        from_attributes = True  # Allows Pydantic to work with SQLAlchemy models
