from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.transaction_schema import TransactionCreate, TransactionResponse
from app.services.transaction_service import TransactionService

router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"]
)

@router.post("/", response_model=TransactionResponse)
async def create_category(transaction_data: TransactionCreate, db: Session = Depends(get_db)):
    service = TransactionService(db)
    transaction = service.create_transaction(transaction_data)
    return transaction

@router.get("/", response_model=list[TransactionResponse])
async def get_all_categories(db: Session = Depends(get_db)):
    service = TransactionService(db)
    transactions = service.get_all_transactions()
    return transactions