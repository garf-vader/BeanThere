from app.db.base_class import Base
from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class User(Base):
    """Represents a user who submits reviews."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(32), nullable=False)
    email: Mapped[str] = mapped_column(String(128), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(256), nullable=False)

    # Relationship to CoffeeReview
    reviews = relationship("CoffeeReview", back_populates="user", lazy=True)
