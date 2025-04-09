from app.database import Base
from sqlalchemy import Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

class Cafe(Base):
    """Represents a coffee shop where reviews can be submitted."""
    __tablename__ = "cafes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    location: Mapped[str | None] = mapped_column(String(100), nullable=True)  # Added location

    # Relationship to CoffeeReview
    reviews = relationship("CoffeeReview", back_populates="cafe", lazy=True)