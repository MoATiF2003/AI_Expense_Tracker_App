from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import Account, Category
from app.schemas.transaction_schema import TransactionCreate

class TransactionValidator:

    VALID_TRANSACTION_TYPES = [
        "income",
        "expense",
        "transfer"
    ]

    def __init__(self, db: Session):
        self.db = db

    def validate(self, transaction_data: TransactionCreate):
        self.validate_amount(transaction_data.amount)
        self.validate_transaction_type(transaction_data.type)
        self.validate_account_exists(transaction_data.account_id)
        if transaction_data.category_id is not None:
            self.validate_category_exists(transaction_data.category_id)

    def validate_amount(self, amount):
        if amount <= 0:
            raise HTTPException(
                status_code=400,
                detail="Amount must be greater than 0"
            )
        
    def validate_transaction_type(self, transaction_type):
        if transaction_type not in self.VALID_TRANSACTION_TYPES:
            raise HTTPException(
                status_code=400,
                detail=(
                    "Transaction type must be "
                    "income, expense or transfer"
                )
            )
        
    def validate_account_exists(self, account_id):
        account = self.db.query(Account).filter(
            Account.id == account_id
        ).first()

        if not account:
            raise HTTPException(
                status_code=404,
                detail="Account not found"
            )
        
    def validate_category_exists(self, category_id):
        category = self.db.query(Category).filter(
            Category.id == category_id
        ).first()

        if not category:
            raise HTTPException(
                status_code=404,
                detail="Category not found"
            )