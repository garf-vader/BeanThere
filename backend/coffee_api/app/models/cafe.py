from app.db.base_class import Base
from geoalchemy2.types import Geography
from geoalchemy2.elements import WKBElement
from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Cafe(Base):
    """Represents a coffee shop where reviews can be submitted."""

    __tablename__ = "cafes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    location: Mapped[WKBElement] = mapped_column(
        Geography(geometry_type="POINT", srid=4326), nullable=False
    )

    # Relationship to CoffeeReview
    reviews = relationship("CoffeeReview", back_populates="cafe", lazy=True)
