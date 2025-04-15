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
    @pytest.mark.parametrize(
        "username, email, password",
        [
            ("JoeBloggs", "joebloggs@email.com", "password123"),
            ("JaneDoe", "janedoe@email.com", "password456"),
            ("Squidward", "squidward@email.com", "clarinet123"),
        ],
    )
    def test_create_user(self, db, username, email, password):
        user_obj = UserCreate(username=username, email=email, password=password)
        user = user_crud.create(db, user_obj)
        assert user.id is not None
        assert user.email == email
        assert user.hashed_password != None

    @pytest.mark.parametrize(
        "existing_user, duplicate_user",
        [
            (
                {
                    "username": "Original",
                    "email": "duplicate@email.com",
                    "password": "pass123",
                },
                {
                    "username": "Copy",
                    "email": "duplicate@email.com",
                    "password": "pass456",
                },
            ),
        ],
    )
    def test_create_user_existing_email(self, db, existing_user, duplicate_user):
        user_crud.create(db, UserCreate(**existing_user))
        with pytest.raises(HTTPException) as exc_info:
            user_crud.create(db, UserCreate(**duplicate_user))
        assert exc_info.value.status_code == 400

    def test_get_user(self, db):
        user = user_crud.get(db, 1)
        assert user is not None
        assert user.id == 1

    @pytest.mark.parametrize(
        "username, email",
        [
            ("EmailLookup", "emailtest1@email.com"),
            ("AnotherLookup", "emailtest2@email.com"),
        ],
    )
    def test_get_by_email(self, db, username, email):
        user_obj = UserCreate(username=username, email=email, password="lookupPass")
        user_crud.create(db, user_obj)
        user = user_crud.get_by_email(db, email)
        assert user is not None
        assert user.username == username

    # strictly speaking this isnt needed, but useful 
    # if I decide to run each test in an isolated DB
    @pytest.mark.parametrize( 
        "users_data",
        [
            [
                {"username": "User1", "email": "user1@email.com", "password": "pass1"},
                {"username": "User2", "email": "user2@email.com", "password": "pass2"},
            ],
        ],
    )
    def test_get_multi_users(self, db, users_data):
        for data in users_data:
            user_crud.create(db, UserCreate(**data))
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

    @pytest.mark.parametrize("nonexistent_id", [999, 1000])
    def test_delete_by_id_not_found(self, db, nonexistent_id):
        with pytest.raises(HTTPException) as exc_info:
            user_crud.delete_by_id(db, nonexistent_id)
        assert exc_info.value.status_code == 404
