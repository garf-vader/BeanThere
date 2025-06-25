from typing import Optional

from pydantic import BaseModel, ConfigDict


class ProximityQuery(BaseModel):
    user_lat: float
    user_lon: float
    search_radius: int
