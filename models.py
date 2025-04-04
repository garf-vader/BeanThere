from database import Base
from sqlalchemy import Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

class Cafe(Base):
    __tablename__ = "cafes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    location: Mapped[str | None] = mapped_column(String(100), nullable=True)  # Added location

    # Relationship to CoffeeReview
    reviews = relationship("CoffeeReview", back_populates="cafe_relation", lazy=True)

class CoffeeReview(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    drinkType: Mapped[str] = mapped_column(String(50), nullable=False)
    roastDarkness: Mapped[int] = mapped_column(Integer, nullable=True)
    tasteRating: Mapped[int] = mapped_column(Integer, nullable=True)
    price: Mapped[float] = mapped_column(Float, nullable=True)
    notes: Mapped[str | None] = mapped_column(String(255), nullable=True)
    cafe: Mapped[int | None] = mapped_column(Integer, ForeignKey("cafes.id"))

    # Relationship to Cafe
    cafe_relation = relationship("Cafe", back_populates="reviews", lazy=False)
