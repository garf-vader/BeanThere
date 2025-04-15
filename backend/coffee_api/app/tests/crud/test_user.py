# tests/crud/
import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.crud.user import user_crud
from app.schemas.user import UserCreate, UserUpdate, UserNewPassword
from app.db.base_class import Base

from app.models import CoffeeReview, Cafe, User

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

class TestUserCRUD:
    def test_create_user(self, db):
        user_data = {
            "username": "JoeBloggs",
            "email": "joebloggs@email.com",
            "password": "password123",
        }
        user_obj = UserCreate(**user_data)
        user = user_crud.create(db, user_obj)
        assert user.id is not None
        assert user.email == "joebloggs@email.com"
        assert user.hashed_password != None

    def test_create_user_existing_email(self, db):
        user_data = {
            "username": "BobHoskins",
            "email": "joebloggs@email.com",
            "password": "randomString",
        }
        user_obj = UserCreate(**user_data)
        with pytest.raises(HTTPException) as exc_info:
            user = user_crud.create(db, user_obj)
        assert exc_info.value.status_code == 400

    def test_get_user(self, db):
        user = user_crud.get(db, 1)
        assert user is not None
        assert user.id == 1

    def test_get_by_email(self, db):
        user_data = {
            "username": "TestName",
            "email": "testemail@email.com",
            "password": "password123",
        }
        user_obj = UserCreate(**user_data)
        user_crud.create(db, user_obj)
        user = user_crud.get_by_email(db, "testemail@email.com")
        assert user is not None
        assert user.username == "TestName"

    def test_get_multi_users(self, db):
        user_data_1 = {
            "username": "JaneDoe",
            "email": "janedoe@email.com",
            "password": "password456",
        }
        user_data_2 = {
            "username": "Squidward",
            "email": "squidwardtentacles@email.com",
            "password": "password789",
        }
        user_obj1 = UserCreate(**user_data_1)
        user_obj2 = UserCreate(**user_data_2)
        user_crud.create(db, user_obj1)
        user_crud.create(db, user_obj2)
        users = user_crud.get_multi(db)
        assert isinstance(users, list)
        assert len(users) >= 1

    def test_new_password(self, db):
        user = user_crud.get(db, 1)
        old_password = user.hashed_password
        update_in = UserNewPassword(password="different_password")
        updated = user_crud.new_password(db, user, update_in)
        new_password = updated.hashed_password
        assert new_password != old_password

    def test_update_user(self, db):
        user = user_crud.get(db, 1)
        old_username = user.username
        update_in = UserUpdate(username="newUsername")
        updated = user_crud.update(db, user, update_in)
        new_username = updated.username
        assert new_username != old_username

    def test_delete_user(self, db):
        user = user_crud.get(db, 1)
        deleted = user_crud.delete(db, user)
        assert deleted.id == 1
        assert user_crud.get(db, 1) is None

    def test_delete_by_id_not_found(self, db):
        with pytest.raises(HTTPException) as exc_info:
            user_crud.delete_by_id(db, 999)
        assert exc_info.value.status_code == 404
