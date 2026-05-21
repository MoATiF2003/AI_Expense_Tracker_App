from sqlalchemy.orm import Session
from difflib import get_close_matches

from app.models import Account

class AccountResolver:

    def __init__(self, db: Session):
        self.db = db

    def resolve(self, account_name: str):
        account = self.db.query(Account).filter(
            Account.name.ilike(account_name)
        ).first()

        return account
    
    def suggest_account(self, account_name: str):
        accounts = self.db.query(Account).all()
        account_names = [account.name for account in accounts]

        matches = get_close_matches(account_name, account_names, n=1, cutoff=0.5)
        if matches:
            return matches[0]
        return None