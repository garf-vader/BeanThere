from typing import Optional

from pydantic import BaseModel, ConfigDict

class CafeCreate(BaseModel):
    name: str
    location: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class CafeUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)