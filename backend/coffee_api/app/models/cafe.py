from app.db.base_class import Base
from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Cafe(Base):
    """Represents a coffee shop where reviews can be submitted."""

    __tablename__ = "cafes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    location: Mapped[str | None] = mapped_column(
        String(100), nullable=True
    )  # Added location

    # Relationship to CoffeeReview
    reviews = relationship("CoffeeReview", back_populates="cafe", lazy=True)
