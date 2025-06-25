from typing import Optional, TypeVar, Type

from pydantic import BaseModel, ConfigDict
from geoalchemy2.shape import to_shape
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.cafe import Cafe


class CafeCreate(BaseModel):
    name: str
    latitude: float
    longitude: float

    model_config = ConfigDict(from_attributes=True)


class CafeUpdate(BaseModel):
    name: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    model_config = ConfigDict(from_attributes=True)


T = TypeVar("T", bound="CafeOut")


class CafeOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    latitude: float
    longitude: float

    @classmethod
    def from_model(cls: Type[T], cafe: "Cafe", **kwargs) -> T:
        point = to_shape(cafe.location)
        longitude, latitude = point.coords[0]

        base_data = {
            "id": cafe.id,
            "name": cafe.name,
            "latitude": latitude,
            "longitude": longitude,
        }

        declared_fields = cls.model_fields.keys()
        unexpected = set(kwargs) - declared_fields
        if unexpected:
            raise ValueError(f"{cls.__name__} got unexpected fields: {unexpected}")

        return cls(**base_data, **kwargs)


class CafeDistance(CafeOut):
    distance: float
