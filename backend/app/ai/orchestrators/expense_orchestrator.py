from app.ai.validators.intent_validator import IntentValidator
from app.ai.validators.slot_validator import SlotValidator
from app.ai.resolvers.account_resolver import AccountResolver
from app.ai.resolvers.category_resolver import CategoryResolver

class ExpenseOrchestrator:

    def __init__(self, intent_agent, slot_agent, db):
        self.intent_agent = intent_agent
        self.slot_agent = slot_agent
        self.account_resolver = AccountResolver(db)
        self.category_resolver = CategoryResolver(db)

    async def process_message(self, message: str):
        intent = await self.intent_agent.detect(message)
        is_valid_intent = IntentValidator.validate(intent=intent)
        if not is_valid_intent:
            return {
                "success": False,
                "error": (
                    "Invalid intent detected"
                ),
                "retry_required": True
            }

        slots = await self.slot_agent.extract(message)
        if intent == "create_transaction":
            validation_result = SlotValidator.validate_transaction_slots(slots=slots)
            if not validation_result["valid"]:
                return {
                    "success": False,
                    "intent": intent,
                    "slots": slots,
                    "error": (
                        validation_result["error"]
                    ),
                    "retry_required": True
                }
            
            resolved_account = self.account_resolver.resolve(slots["account"])
            resolved_category = self.category_resolver.resolve(slots["category"])

            if not resolved_account:
                return {
                    "success": False,
                    "intent": intent,
                    "slots": slots,
                    "error": "Account not found",
                    "retry_required": True
                }
            
            if not resolved_category:
                return {
                    "success": False,
                    "intent": intent,
                    "slots": slots,
                    "error": "Category not found",
                    "retry_required": True
                }
            
            slots["account_id"] = resolved_account.id
            slots["category_id"] = resolved_category.id

        return {
            "success": True,
            "intent": intent,
            "slots": slots,
            "requires_confirmation": True 
        }