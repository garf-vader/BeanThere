# tests/crud/
import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.crud.cafe import cafe_crud
from app.schemas.cafe import CafeCreate, CafeUpdate
from app.db.base_class import Base

from app.models import CoffeeReview, Cafe, User

from fastapi import HTTPException

# Currently no option for engine as migration to Postgres in progress
engine = create_engine(##)
TestingSessionLocal = sessionmaker(bind=engine)


@pytest.fixture(scope="module")
def db():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

class TestCafeCRUD:
    def test_get_by_proximity_no_results(self, db):
        user_location = "POINT(0 0)"
        search_radius = 1000

        results = cafe_crud.get_by_proximity(
            db=db, user_location=user_location, search_radius=search_radius
        )
        assert results == []

    def test_get_by_proximity_with_results(self, db):
        user_location = "POINT(0 0)"
        search_radius = 1000

        # Mock Cafe data
        cafe = Cafe(name="Test Cafe", location="POINT(0.001 0.001)")
        cafe_crud.create(db = db, obj_in = cafe)

        results = cafe_crud.get_by_proximity(
            db=db, user_location=user_location, search_radius=search_radius
        )
        assert len(results) > 0
        assert results[0].name == "Test Cafe"