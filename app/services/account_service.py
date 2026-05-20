from sqlalchemy.orm import Session

from app.repositories.account_repository import AccountRepository
from app.schemas.account_schema import AccountCreate

class AccountService:

    def __init__(self, db: Session):
        self.repository = AccountRepository(db)

    def create_account(
        self,
        account_data: AccountCreate
    ):
        return self.repository.create_account(account_data)
    
    def get_all_accounts(self):
        return self.repository.get_all_accounts()