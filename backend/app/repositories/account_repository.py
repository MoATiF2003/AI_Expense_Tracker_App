from sqlalchemy.orm import Session

from app.models import Account
from app.schemas.account_schema import AccountCreate


class AccountRepository:

    def __init__(self, db: Session):
        self.db = db


    def create_account(
        self,
        account_data: AccountCreate
    ) -> Account:

        account = Account(
            name=account_data.name,
            type=account_data.type,
            opening_balance=account_data.opening_balance
        )
        self.db.add(account)
        self.db.commit()
        self.db.refresh(account)

        return account