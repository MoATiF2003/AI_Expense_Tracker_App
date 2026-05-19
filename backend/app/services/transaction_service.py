from sqlalchemy.orm import Session

from app.repositories.transaction_repository import TransactionRepository
from app.schemas.transaction_schema import TransactionCreate

class TransactionService:

    def __init__(self, db: Session):
        self.repository = TransactionRepository(db)

    def create_transaction(
            self,
            transaction_data: TransactionCreate
    ):
        return self.repository.create_transaction(transaction_data)
    
    def get_all_transactions(self):
        return self.repository.get_all_transaction()