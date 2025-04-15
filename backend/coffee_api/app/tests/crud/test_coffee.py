# tests/crud/
import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.crud.coffee import coffee_crud
from app.models.coffee import CoffeeReview
from app.schemas.coffee import CoffeeReviewCreate, CoffeeReviewUpdate
from app.db.base_class import Base

from fastapi import HTTPException

# Setup in-memory SQLite test database
engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(bind=engine)


@pytest.fixture(scope="module")
def db():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

class TestCoffeeCRUD:
    def test_create_review(self, db):
        review_data = {
            "drinkType": "Latte",
            "roastDarkness": 3,
            "tasteRating": 4,
            "price": 3.5,
            "notes": "Smooth with a hint of caramel",
            #"cafeId": 0,
            #"userId": 0,
        }
        review_obj = CoffeeReviewCreate(**review_data)
        review = coffee_crud.create(db, review_obj)
        assert review.id is not None
        assert review.tasteRating == 4
        assert review.notes == "Smooth with a hint of caramel"

    def test_get_review(self, db):
        review = coffee_crud.get(db, 1)
        assert review is not None
        assert review.id == 1

    def test_get_multi_reviews(self, db):
        review_data_1 = {
            "drinkType": "Americano",
            "roastDarkness": 3,
            "tasteRating": 5,
            "price": 3.25,
            "notes": "Bloody Lovely!",
        }
        review_data_2 = {
            "drinkType": "Espresso",
            "roastDarkness": 1,
            "tasteRating": 1,
            "price": 1.5,
            "notes": "Rubbish",
        }
        review_obj1 = CoffeeReviewCreate(**review_data_1)
        review_obj2 = CoffeeReviewCreate(**review_data_2)
        coffee_crud.create(db, review_obj1)
        coffee_crud.create(db, review_obj2)
        reviews = coffee_crud.get_multi(db)
        assert isinstance(reviews, list)
        assert len(reviews) >= 1

    def test_update_review(self, db):
        review = coffee_crud.get(db, 1)
        update_in = CoffeeReviewUpdate(notes="Rich and chocolatey.")
        updated = coffee_crud.update(db, review, update_in)
        assert updated.notes == "Rich and chocolatey."

    def test_delete_review(self, db):
        review = coffee_crud.get(db, 1)
        deleted = coffee_crud.delete(db, review)
        assert deleted.id == 1
        assert coffee_crud.get(db, 1) is None

    def test_delete_by_id_not_found(self, db):
        with pytest.raises(HTTPException) as exc_info:
            coffee_crud.delete_by_id(db, 999)
        assert exc_info.value.status_code == 404
