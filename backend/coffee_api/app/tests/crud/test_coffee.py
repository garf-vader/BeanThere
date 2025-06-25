# tests/crud/
import pytest

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import StaticPool, NullPool

from app.crud.coffee import coffee_crud
from app.schemas.coffee import CoffeeReviewCreate, CoffeeReviewUpdate
from app.db.base_class import Base

from app.models import CoffeeReview, Cafe, User

from fastapi import HTTPException


# This will automatically start and stop a PostgreSQL container for tests
@pytest.fixture(scope="function")
def db(postgresql):
    """Create a clean database session for a test."""
    connection_url = (
        f"postgresql+psycopg2://{postgresql.info.user}:@{postgresql.info.host}:"
        f"{postgresql.info.port}/{postgresql.info.dbname}"
    )

    engine = create_engine(connection_url, echo=False, poolclass=NullPool)

    with engine.begin() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS postgis"))

    Base.metadata.create_all(engine)

    Session = scoped_session(sessionmaker(bind=engine))
    session = Session()

    yield session  # Provide the test with a usable session

    session.close()
    Session.remove()
    Base.metadata.drop_all(engine)


def sample_review_data(
    drinkType="Latte",
    roastDarkness=3,
    tasteRating=4,
    price=3.5,
    notes="Smooth with a hint of caramel",
):
    return {
        "drinkType": drinkType,
        "roastDarkness": roastDarkness,
        "tasteRating": tasteRating,
        "price": price,
        "notes": notes,
    }


class TestCoffeeCRUD:
    def test_create_review(self, db):
        review_obj = CoffeeReviewCreate(**sample_review_data())
        review = coffee_crud.create(db, review_obj)
        assert review.id is not None
        assert review.tasteRating == 4
        assert review.notes == "Smooth with a hint of caramel"

    def test_get_review(self, db):
        review_obj = CoffeeReviewCreate(
            **sample_review_data(
                drinkType="Americano", tasteRating=5, notes="Bloody Lovely!"
            )
        )
        review = coffee_crud.create(db, review_obj)
        fetched = coffee_crud.get(db, review.id)
        assert fetched is not None
        assert fetched.id == review.id

    def test_get_multi_reviews(self, db):
        review_obj1 = CoffeeReviewCreate(
            **sample_review_data(
                drinkType="Americano", tasteRating=5, notes="Bloody Lovely!"
            )
        )
        review_obj2 = CoffeeReviewCreate(
            **sample_review_data(
                drinkType="Espresso",
                roastDarkness=1,
                tasteRating=1,
                price=1.5,
                notes="Rubbish",
            )
        )
        coffee_crud.create(db, review_obj1)
        coffee_crud.create(db, review_obj2)
        reviews = coffee_crud.get_multi(db)
        assert isinstance(reviews, list)
        assert len(reviews) >= 2

    def test_update_review(self, db):
        review_obj = CoffeeReviewCreate(**sample_review_data())
        review = coffee_crud.create(db, review_obj)
        update_in = CoffeeReviewUpdate(notes="Rich and chocolatey.")
        updated = coffee_crud.update(db, review, update_in)
        assert updated.notes == "Rich and chocolatey."

    def test_delete_review(self, db):
        review_obj = CoffeeReviewCreate(**sample_review_data())
        review = coffee_crud.create(db, review_obj)
        deleted = coffee_crud.delete(db, review)
        assert deleted.id == review.id
        assert coffee_crud.get(db, review.id) is None

    def test_delete_by_id_not_found(self, db):
        with pytest.raises(HTTPException) as exc_info:
            coffee_crud.delete_by_id(db, 999)
        assert exc_info.value.status_code == 404
