from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

from app.models import Account
from app.schemas.account_schema import AccountCreate


class AccountRepository:

    def __init__(self, db: Session):
        self.db = db


    def create_account(
        self,
        account_data: AccountCreate
    ) -> Account:

        try:
            account = Account(
                name=account_data.name,
                type=account_data.type,
                opening_balance=account_data.opening_balance
            )
            self.db.add(account)
            self.db.commit()
            self.db.refresh(account)

            return account
        
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=404,
                detail="Account name already exists"
            )
        
        except Exception:
            self.db.rollback()
            raise HTTPException(
                status_code=500,
                detail="Database error"
            )
        
    def get_all_accounts(self):
        return self.db.query(Account).all()
