from typing import Optional

from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserInDB, UserNewPassword
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.security import Hasher

from fastapi import HTTPException


class UserCRUD(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        """
        Simple function to retrieve user by email address

        Prevents code reuse, and ensures uniformity
        """
        stmt = select(User).where(User.email == email)
        return db.execute(stmt).scalars(stmt).first()

    def create(self, db: Session, obj_in: UserCreate) -> User:
        # Check if the email already exists in the database
        existing_user = self.get_by_email(db=db, email=obj_in.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        # If Email is unique, hash password and create user
        hashed_password = Hasher.get_password_hash(obj_in.password)

        user_data = obj_in.model_dump(exclude={"password"})
        user_data["hashed_password"] = hashed_password

        db_obj = self.model(**user_data)

        # Add the object to the DB session, commit, and return the object
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def new_password(self, db: Session, db_obj: User, obj_in: UserNewPassword) -> User:
        if Hasher.verify_password(obj_in.password, db_obj.hashed_password):
            raise HTTPException(status_code=400, detail="Cannot use existing password")
        
        new_hashed_password = Hasher.get_password_hash(obj_in.password)
        db_obj.hashed_password = new_hashed_password
        db.commit()
        db.refresh(db_obj)
        return db_obj

user_crud = UserCRUD(model=User)