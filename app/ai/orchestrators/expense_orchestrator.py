from app.ai.validators.intent_validator import IntentValidator
from app.ai.validators.slot_validator import SlotValidator
from app.ai.resolvers.account_resolver import AccountResolver
from app.ai.resolvers.category_resolver import CategoryResolver
from app.ai.resolvers.semantic_category_resolver import SemanticCategoryResolver
from app.services.category_service import CategoryService
from app.ai.utils.clarification_generator import ClarificationGenerator

class ExpenseOrchestrator:

    def __init__(self, intent_agent, slot_agent, db):
        self.intent_agent = intent_agent
        self.slot_agent = slot_agent
        self.db = db
        self.account_resolver = AccountResolver(db)
        self.category_resolver = CategoryResolver(db)
        self.semantic_category_resolver = SemanticCategoryResolver(intent_agent.llm_provider)


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
        response = {
            "success": True,
            "intent": intent,
            "slots": slots,
            "requires_confirmation": True
        }
        if intent == "create_transaction":
            validation_result = SlotValidator.validate_transaction_slots(slots=slots)
            if not validation_result["valid"]:
                if validation_result.get("requires_clarification"):
                    clarification_question = ClarificationGenerator.generate_question(
                        validation_result["missing_fields"]
                    )

                    return {
                        "success": False,
                        "intent": intent,
                        "slots": slots,
                        "missing_fields": validation_result["missing_fields"],
                        "clarification_question": clarification_question,
                        "requires_clarification": True               
                    }

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
            # resolved_category = self.category_resolver.resolve(slots["category"])

            if not resolved_account:
                return {
                    "success": False,
                    "intent": intent,
                    "slots": slots,
                    "error": "Account not found",
                    "retry_required": True
                }
            
            # if not resolved_category:
            #     return {
            #         "success": False,
            #         "intent": intent,
            #         "slots": slots,
            #         "error": "Category not found",
            #         "retry_required": True
            # }
            
            slots["account_id"] = resolved_account.id
            # slots["category_id"] = resolved_category.id

            category_service = CategoryService(self.db)
            existing_categories = category_service.get_category_names()
            category_resolution = await self.semantic_category_resolver.resolve_category(
                user_message=message,
                existing_categories=existing_categories
            )
            matched_category = category_resolution["matched_category"]
            proposed_new_category = category_resolution["proposed_new_category"]

            if matched_category:
                resolved_category = self.category_resolver.resolve(category_name=matched_category)
                if resolved_category:
                    slots["category"] = matched_category
                    slots["category_id"] = resolved_category.id

            if proposed_new_category:
                response["proposed_new_category"] = {
                        "name": proposed_new_category,
                        "type": slots["transaction_type"]
                }
            

        return response