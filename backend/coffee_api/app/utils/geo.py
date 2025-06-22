from geoalchemy2 import WKTElement


def point_from_latlon(latitude: float, longitude: float, srid: int = 4326) -> WKTElement:
    return WKTElement(f"POINT({longitude} {latitude})", srid=srid)
