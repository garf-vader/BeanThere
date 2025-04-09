from pydantic import BaseModel
from typing import Optional

# Pydantic model for User
class UserCreate(BaseModel):
    username: str
    email: str

    class Config:
        from_attributes = True  # Allows Pydantic to work with SQLAlchemy models

# Seperation of concerns, keep hashed password seperate
# Represents the data stored in the database, including sensitive fields
class UserInDB(UserCreate):
    hashed_password: str