from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.account_schema import AccountCreate, AccountResponse
from app.services.account_service import AccountService

router = APIRouter(
    prefix='/accounts',
    tags=["Accounts"]
)

@router.post("/", response_model=AccountResponse)
async def create_account(account_data: AccountCreate, db: Session = Depends(get_db)):
    service = AccountService(db)
    account = service.create_account(account_data)
    return account

@router.get("/", response_model=list[AccountResponse])
async def get_all_account(db: Session = Depends(get_db)):
    service = AccountService(db)
    accounts = service.get_all_accounts()
    return accounts