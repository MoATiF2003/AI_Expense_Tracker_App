from sqlalchemy.orm import Session

from app.models import Transaction
from app.schemas.transaction_schema import TransactionCreate

class TransactionRepository:

    def __init__(self, db: Session):
        self.db = db

    def create_transaction(
            self,
            transaction_data: TransactionCreate,
    ) -> Transaction:
        
        transaction = Transaction(
            type=transaction_data.type,
            amount=transaction_data.amount,
            category_id=transaction_data.category_id,
            account_id=transaction_data.account_id,
            transfer_id=transaction_data.transfer_id,
            description=transaction_data.description,
            date=transaction_data.date
        )
        self.db.add(transaction)
        self.db.commit()
        self.db.refresh(transaction)

        return transaction