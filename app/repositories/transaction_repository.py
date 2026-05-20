from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

from app.models import Transaction
from app.schemas.transaction_schema import TransactionCreate

class TransactionRepository:

    def __init__(self, db: Session):
        self.db = db

    def create_transaction(
            self,
            transaction_data: TransactionCreate,
    ) -> Transaction:
        
        try:
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
        
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=400,
                detail="Invalid transaction data"
            )

        except Exception:
            self.db.rollback()
            raise HTTPException(
                status_code=500,
                detail="Database error"
            )          
        
    def get_all_transaction(self):
        return self.db.query(Transaction).all()