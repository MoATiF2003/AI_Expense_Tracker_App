from app.models import Category
from app.schemas.transaction_schema import TransactionCreate
from app.services.category_service import CategoryService
from app.services.transaction_service import TransactionService

from datetime import date

class AIExecutionService:

    def __init__(self, db):
        self.db = db
        self.category_service = CategoryService(db)
        self.transaction_service = TransactionService(db)

    def execute_transaction(self, slots, proposed_new_category=None):
        if proposed_new_category:
            new_category = self.category_service.create_category(
                Category(
                    name=proposed_new_category.name,
                    type=proposed_new_category.type
                )
            )

            slots["category_id"] = new_category.id
            slots["category"] = new_category.name
        
        transaction_data = TransactionCreate(
            type=slots["transaction_type"],
            amount=slots["amount"],
            category_id=slots["category_id"],
            account_id=slots["account_id"],
            description=slots.get("description"),
            date=slots.get("date", date.today())
        )
        transaction = self.transaction_service.create_transaction(transaction_data=transaction_data)

        return transaction