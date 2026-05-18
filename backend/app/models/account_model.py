from sqlalchemy import Numeric, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from decimal import Decimal
from app.models.base import Base

class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    type: Mapped[str] = mapped_column(
        String(50),
        nullable=True
    )

    opening_balance: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        default=Decimal("0.00")
    )

    transactions = relationship(
        "Transaction",
        back_populates="account"
    )