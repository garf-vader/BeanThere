from geoalchemy2 import WKTElement
from geoalchemy2.elements import WKBElement
from shapely import Point


def point_from_latlon(latitude: float, longitude: float, srid: int = 4326) -> WKTElement:
    return WKTElement(f"POINT({longitude} {latitude})", srid=srid)

def wkb_from_latlon(latitude: float, longitude: float, srid: int = 4326) -> WKBElement:
    point = Point(longitude, latitude)
    return WKBElement(point.wkb, srid=srid)
