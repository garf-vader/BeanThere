from app.database import Base
from sqlalchemy import Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

class CoffeeReview(Base):
    """Represents a review of a specific coffee from a cafe."""
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    drinkType: Mapped[str] = mapped_column(String(50), nullable=False)
    roastDarkness: Mapped[int] = mapped_column(Integer, nullable=True)
    tasteRating: Mapped[int] = mapped_column(Integer, nullable=True)
    price: Mapped[float] = mapped_column(Float, nullable=True)
    notes: Mapped[str | None] = mapped_column(String(255), nullable=True)
    cafeId: Mapped[int | None] = mapped_column(Integer, ForeignKey("cafes.id"))
    userId: Mapped[int | None] = mapped_column(Integer, ForeignKey("users.id"))

    # Relationship to Cafe
    cafe = relationship("Cafe", back_populates="reviews", lazy=False)
    user = relationship("User", back_populates="reviews", lazy=False)