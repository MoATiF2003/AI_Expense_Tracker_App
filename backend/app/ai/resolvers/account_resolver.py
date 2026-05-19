from sqlalchemy.orm import Session

from app.models import Account

class AccountResolver:

    def __init__(self, db: Session):
        self.db = db

    def resolve(self, account_name: str):
        account = self.db.query(Account).filter(
            Account.name.ilike(account_name)
        ).first()

        return account