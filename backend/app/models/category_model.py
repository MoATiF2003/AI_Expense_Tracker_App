from sqlalchemy import Integer, Float, String
from sqlalchemy.orm import mapped_column, relationship, Mapped

from app.models.base import Base

class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True
    )

    type: Mapped[str] = mapped_column(
        String(50),
        nullable=True
    )

    transactions = relationship(
        "Transaction",
        back_populates="category"
    )