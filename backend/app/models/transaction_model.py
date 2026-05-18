from sqlalchemy import (
    Integer,
    Text,
    Numeric,
    ForeignKey,
    String,
    Date
)
from sqlalchemy.orm import mapped_column, relationship, Mapped
from decimal import Decimal

from app.models.base import Base

from datetime import date

class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    type: Mapped[str] = mapped_column(
        String(50),
        nullable=True
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False
    )

    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id"),
        nullable=True
    )

    account_id: Mapped[int] = mapped_column(
        ForeignKey("accounts.id"),
        nullable=False
    )

    transfer_id: Mapped[str] = mapped_column(
        String(50),
        nullable=True
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=True
    )

    date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    category = relationship(
        "Category",
        back_populates="transactions"
    )

    account = relationship(
        "Account",
        back_populates="transactions"
    )