from datetime import date
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel #base class that you inherit from to define data schemas

from app.schemas.account_schema import AccountBasicResponse
from app.schemas.category_schema import CategoryBasicResponse

class TransactionCreate(BaseModel):
    type: Optional[str] = None

    amount: Decimal

    category_id: Optional[int] = None

    account_id: int

    transfer_id: Optional[int] = None

    description: Optional[str] = None

    date: date

class TransactionResponse(BaseModel):
    id: int

    type: Optional[str] 

    amount: Decimal

    category_id: Optional[int] 

    account_id: int

    transfer_id: Optional[int] 

    description: Optional[str] 

    date: date

    category: Optional[CategoryBasicResponse]

    account: AccountBasicResponse

    class Config:
        from_attributes = True