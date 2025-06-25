# tests/crud/
import pytest

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.orm.session import Session
from sqlalchemy.pool import StaticPool, NullPool

from app.crud.cafe import cafe_crud
from app.schemas.cafe import CafeCreate, CafeUpdate
from app.db.base_class import Base

from app.models import Cafe
from app.models.cafe import Cafe
from geoalchemy2 import WKTElement
from app.schemas.cafe import CafeOut
from app.models.cafe import Cafe
from geoalchemy2 import WKTElement
from app.schemas.cafe import CafeDistance
from app.models.cafe import Cafe
from geoalchemy2 import WKTElement
from app.schemas.cafe import CafeOut
from app.utils.geo import point_from_latlon, wkb_from_latlon


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


class TestCafeCRUD:
    def test_create_and_get_cafe(self, db: Session):
        cafe_in = CafeCreate(name="Cafe Alpha", latitude=1, longitude=1)
        cafe = cafe_crud.create(db=db, obj_in=cafe_in)
        assert cafe.id is not None
        fetched = cafe_crud.get(db, cafe.id)
        assert fetched is not None
        assert fetched.name == "Cafe Alpha"

    def test_update_cafe(self, db: Session):
        cafe_in = CafeCreate(name="Cafe Beta", latitude=2, longitude=2)
        cafe = cafe_crud.create(db=db, obj_in=cafe_in)
        update_in = CafeUpdate(name="Cafe Beta Updated")
        updated = cafe_crud.update(db, cafe, update_in)
        assert updated.name == "Cafe Beta Updated"

    def test_delete_cafe(self, db: Session):
        cafe_in = CafeCreate(name="Cafe Gamma", latitude=3, longitude=3)
        cafe = cafe_crud.create(db=db, obj_in=cafe_in)
        cafe_id = cafe.id
        cafe_crud.delete_by_id(db, cafe_id)
        assert cafe_crud.get(db, cafe_id) is None

    def test_get_by_proximity_no_results(self, db: Session):
        # Assuming no cafes near this point
        user_lat, user_lon, search_radius = 0, 0, 100
        results = cafe_crud.get_by_proximity(
            db=db, user_lat=user_lat, user_lon=user_lon, search_radius=search_radius
        )
        assert results == []

    def test_get_by_proximity_with_results(self, db: Session):
        # Create a cafe near the search point
        cafe_in = CafeCreate(name="Nearby Cafe", latitude=0.001, longitude=0.001)
        cafe_crud.create(db=db, obj_in=cafe_in)
        user_lat, user_lon, search_radius = 0, 0, 100000  # Large radius
        results = cafe_crud.get_by_proximity(
            db=db, user_lat=user_lat, user_lon=user_lon, search_radius=search_radius
        )
        assert any(c[0].name == "Nearby Cafe" for c in results)

    def test_get_by_proximity_partial_results(self, db: Session):
        # Create 3 cafes: 2 nearby, 1 far away
        cafe_crud.create(db=db, obj_in=CafeCreate(name="Near Cafe 1", latitude=0.001, longitude=0.001))
        cafe_crud.create(db=db, obj_in=CafeCreate(name="Near Cafe 2", latitude=0.002, longitude=0.002))
        cafe_crud.create(db=db, obj_in=CafeCreate(name="Far Cafe", latitude=10, longitude=10))

        user_lat = 0
        user_lon = 0
        search_radius = 500000  # Large enough for near cafes, too small for far cafe

        results = cafe_crud.get_by_proximity(
            db=db, user_lat=user_lat, user_lon=user_lon, search_radius=search_radius
        )
        print(results)
        result_names = [cafe.name for cafe, _ in results]
        assert "Near Cafe 1" in result_names
        assert "Near Cafe 2" in result_names
        assert "Far Cafe" not in result_names
        assert len(result_names) == 2

    def test_cafeout_from_model_basic(self):
        # Create a fake Cafe model instance
        cafe = Cafe(id=1, name="Test Cafe")
        # Simulate a Point geometry (longitude, latitude)
        point = wkb_from_latlon(latitude=56.78, longitude=12.34)
        cafe.location = point

        cafe_out = CafeOut.from_model(cafe)
        assert cafe_out.id == 1
        assert cafe_out.name == "Test Cafe"
        assert cafe_out.latitude == 56.78
        assert cafe_out.longitude == 12.34

    def test_cafeout_from_model_with_extra_kwargs(self):

        cafe = Cafe(id=2, name="Distance Cafe")
        point = wkb_from_latlon(latitude=4.56, longitude=1.23)
        cafe.location = point

        cafe_distance = CafeDistance.from_model(cafe, distance=123.45)
        assert cafe_distance.id == 2
        assert cafe_distance.name == "Distance Cafe"
        assert cafe_distance.latitude == 4.56
        assert cafe_distance.longitude == 1.23
        assert cafe_distance.distance == 123.45

    def test_cafeout_from_model_unexpected_kwargs_raises(self):

        cafe = Cafe(id=3, name="Bad Cafe")
        point = wkb_from_latlon(latitude=0, longitude=0)
        cafe.location = point

        with pytest.raises(ValueError) as excinfo:
            CafeOut.from_model(cafe, not_a_field=1)
