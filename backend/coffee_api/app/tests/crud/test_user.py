# tests/crud/
import pytest

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import StaticPool, NullPool

from app.crud.user import user_crud
from app.schemas.user import UserCreate, UserUpdate, UserNewPassword
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


@pytest.mark.parametrize(
    "username, email, password",
    [
        ("JoeBloggs", "joebloggs@email.com", "password123"),
        ("JaneDoe", "janedoe@email.com", "password456"),
        ("Squidward", "squidward@email.com", "clarinet123"),
    ],
)
class TestUserCreation:
    def test_create_user(self, db, username, email, password):
        user_obj = UserCreate(username=username, email=email, password=password)
        user = user_crud.create(db, user_obj)
        assert user.id is not None
        assert user.email == email
        assert user.hashed_password != None

    def test_create_user_existing_email(self, db, username, email, password):
        user_obj = UserCreate(username=username, email=email, password=password)
        user = user_crud.create(db, user_obj)
        with pytest.raises(HTTPException) as exc_info:
            duplicate_data = UserCreate(username="Copy", email=email, password="Copy")
            user_crud.create(db, duplicate_data)
        assert exc_info.value.status_code == 400


class TestUserCRUDWithPrepopulatedDB:
    @pytest.fixture(autouse=True)
    def create_users(self, db):
        users_data = [
            {"username": "alice", "email": "alice@email.com", "password": "password1"},
            {"username": "bob", "email": "bob@email.com", "password": "password2"},
            {"username": "carol", "email": "carol@email.com", "password": "password3"},
        ]
        for data in users_data:
            user_crud.create(db, UserCreate(**data))

    def test_get_user(self, db):
        user = user_crud.get(db, 1)
        assert user is not None
        assert user.id == 1

    @pytest.mark.parametrize(
        "username, email",
        [
            ("alice", "alice@email.com"),
            ("bob", "bob@email.com"),
            ("carol", "carol@email.com"),
        ],
    )
    def test_get_by_email(self, db, username, email):
        user = user_crud.get_by_email(db, email)
        assert user is not None
        assert user.username == username

    def test_get_multi_users(self, db):
        users = user_crud.get_multi(db)
        assert isinstance(users, list)
        assert len(users) >= 1

    def test_new_password(self, db):
        user = user_crud.get(db, 1)
        assert user is not None
        old_password = user.hashed_password
        update_in = UserNewPassword(password="different_password")
        updated = user_crud.new_password(db, user, update_in)
        new_password = updated.hashed_password
        assert new_password != old_password

    def test_update_user(self, db):
        user = user_crud.get(db, 1)
        assert user is not None
        old_username = user.username
        update_in = UserUpdate(username="newUsername")
        updated = user_crud.update(db, user, update_in)
        new_username = updated.username
        assert new_username != old_username

    def test_delete_user(self, db):
        user = user_crud.get(db, 1)
        assert user is not None
        deleted = user_crud.delete(db, user)
        assert deleted.id == 1
        assert user_crud.get(db, 1) is None

    @pytest.mark.parametrize("nonexistent_id", [999, 1000])
    def test_delete_by_id_not_found(self, db, nonexistent_id):
        with pytest.raises(HTTPException) as exc_info:
            user_crud.delete_by_id(db, nonexistent_id)
        assert exc_info.value.status_code == 404


@pytest.mark.parametrize(
    "username, email, password",
    [
        ("AlfaBravo", "ab@email.com", "pass1"),
        ("CharlieDelta", "cd@email.com", "pass2"),
        ("EchoFoxtrot", "ef@email.com", "pass3"),
    ],
)
class TestUserAuthentication:
    def test_authenticate_login(self, db, username, email, password):
        user_obj = UserCreate(username=username, email=email, password=password)
        user = user_crud.create(db, user_obj)
        auth_user = user_crud.authenticate_login(db, email=email, password=password)
        assert auth_user is not None
        assert auth_user.username == username
        assert auth_user.email == email
        assert auth_user.hashed_password == user.hashed_password

    def test_authenticate_login_email_failure(self, db, username, email, password):
        user_obj = UserCreate(username=username, email=email, password=password)
        user = user_crud.create(db, user_obj)
        auth_user = user_crud.authenticate_login(
            db, email="wrongemail@email.com", password=password
        )
        assert auth_user is None

    def test_authenticate_login_wrong_password(self, db, username, email, password):
        user_obj = UserCreate(username=username, email=email, password="wrongPassword")
        user = user_crud.create(db, user_obj)
        auth_user = user_crud.authenticate_login(db, email=email, password=password)
        assert auth_user is None
