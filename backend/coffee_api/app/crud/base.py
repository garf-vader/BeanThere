# Common CRUD operations stored here, simplifies management of new operations
# DRY, no point having an identical objectCreate function in every CRUD file

from typing import Generic, TypeVar, Type, Optional, List
from sqlalchemy.orm import Session
from pydantic import BaseModel
from sqlalchemy import select
from fastapi import HTTPException

from app.database import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """CRUD object with default methods to Create, Read, Update, Delete (CRUD)

    **Parameters**
    * "model" : A SQLAlchemy model class
    * `schema`: A Pydantic model (schema) class

    """

    def __init__(self, model: Type[ModelType]):
        """Initialises CRUDBase using a model within app.models"""
        self.model = model

    def get(self, db: Session, id: int) -> Optional[ModelType]:
        return db.get(self.model, id)

    def get_multi(
        self, db: Session, skip: int = 0, limit: int = 5000
    ) -> List[ModelType]:
        stmt = select(self.model).offset(skip).limit(limit)
        return db.execute(stmt).scalars().all()

    def create(self, db: Session, obj_in: CreateSchemaType) -> ModelType:
        create_data = obj_in.model_dump(exclude_none=True, exclude_unset=True)
        db_obj = self.model(**create_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, db_obj: ModelType, obj_in: UpdateSchemaType
    ) -> ModelType:
        update_data = obj_in.model_dump(exclude_none=True, exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, obj_in: ModelType) -> ModelType:
        # obj = db.get(self.model, id)
        # if obj is None:
        #    raise HTTPException(status_code=404, detail=f"{self.model.__name__} not found")
        db.delete(obj_in)
        db.commit()
        return obj_in

    def delete_by_id(self, db: Session, id: int) -> ModelType:
        obj = db.get(self.model, id)
        if obj is None:
            raise HTTPException(
                status_code=404, detail=f"{self.model.__name__} not found"
            )
        db.delete(obj)
        db.commit()
        return obj
