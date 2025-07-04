from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr

class UserBase(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None

# Pydantic model for User
class UserCreate(UserBase):
    username: str
    email: EmailStr
    password: str

class UserUpdate(UserBase):
    username: Optional[str] = None

class UserNewPassword(UserBase):
    password: Optional[str] = None

# Seperation of concerns, keep hashed password seperate
class UserInDB(UserBase):
    hashed_password: str
    model_config = ConfigDict(from_attributes=True)

class UserOut(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)