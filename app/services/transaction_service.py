from sqlalchemy.orm import Session

from app.repositories.transaction_repository import TransactionRepository
from app.schemas.transaction_schema import TransactionCreate
from app.validators.transaction_validator import TransactionValidator

class TransactionService:

    def __init__(self, db: Session):
        self.repository = TransactionRepository(db)
        self.validator = TransactionValidator(db)

    def create_transaction(self, transaction_data: TransactionCreate):
        self.validator.validate(transaction_data)

        return self.repository.create_transaction(transaction_data)
    
    def get_all_transactions(self):
        return self.repository.get_all_transaction()