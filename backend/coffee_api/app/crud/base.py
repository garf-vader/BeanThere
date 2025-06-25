# Common CRUD operations stored here, simplifies management of new operations
# DRY, no point having an identical objectCreate function in every CRUD file

from typing import Generic, TypeVar, Type, Optional, List
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import DeclarativeMeta
from pydantic import BaseModel
from sqlalchemy import Sequence, select
from fastapi import HTTPException

ModelType = TypeVar("ModelType", bound=DeclarativeMeta)
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
    ) -> list[ModelType]:
        stmt = select(self.model).offset(skip).limit(limit)
        return db.execute(stmt).scalars().all()

    def _preprocess_input(self, data: dict) -> dict:
        """Override this in subclasses to modify data before create/update."""
        return data

    def create(self, db: Session, obj_in: CreateSchemaType) -> ModelType:
        # Take user input and convert to a dict
        input_data = obj_in.model_dump(exclude_none=True, exclude_unset=True)
        # Take the user input and preprocess it, this allows for human readable input to be converted e.g. lat/lon to geospatial point
        create_data = self._preprocess_input(input_data)
        db_obj = self.model(**create_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, db_obj: ModelType, obj_in: UpdateSchemaType
    ) -> ModelType:
        # Take user input and convert to a dict
        input_data = obj_in.model_dump(exclude_none=True, exclude_unset=True)
        # Take the user input and preprocess it, this allows for human readable input to be converted e.g. lat/lon to geospatial point
        update_data = self._preprocess_input(input_data)
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
