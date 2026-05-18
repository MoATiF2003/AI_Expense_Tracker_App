from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class AccountCreate(BaseModel):
    name: str

    type: Optional[str] = None

    opening_balance: Decimal = Decimal("0.00")


class AccountResponse(BaseModel):
    id: int

    name: str

    type: Optional[str]

    opening_balance: Decimal

    class Config:
        from_attributes = True