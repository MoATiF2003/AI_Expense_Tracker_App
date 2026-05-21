from app.ai.validators.intent_validator import IntentValidator
from app.ai.validators.slot_validator import SlotValidator
from app.ai.resolvers.account_resolver import AccountResolver
from app.ai.resolvers.category_resolver import CategoryResolver
from app.ai.resolvers.semantic_category_resolver import SemanticCategoryResolver
from app.services.category_service import CategoryService
from app.ai.utils.clarification_generator import ClarificationGenerator
from app.ai.state.conversation_state_manager import ConversationStateManager
from app.ai.validators.clarification_validator import ClarificationValidator
from app.services.account_service import AccountService
from app.ai.presenters.confirmation_presenter import ConfirmationPresenter
class ExpenseOrchestrator:

    def __init__(self, intent_agent, slot_agent, db):
        self.intent_agent = intent_agent
        self.slot_agent = slot_agent
        self.db = db
        self.account_resolver = AccountResolver(db)
        self.category_resolver = CategoryResolver(db)
        self.semantic_category_resolver = SemanticCategoryResolver(intent_agent.llm_provider)


    async def process_message(self, session_id: str, message: str):
        pending_workflow = ConversationStateManager.get_workflow(session_id=session_id)
        if pending_workflow:
            return await self.handle_clarification(
                session_id=session_id,
                message=message,
                pending_workflow=pending_workflow
            )

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
            "requires_confirmation": True,
            "confirmation_summary": None
        }
        if intent == "create_transaction":
            validation_result = SlotValidator.validate_transaction_slots(slots=slots)
            if not validation_result["valid"]:
                if validation_result.get("requires_clarification"):
                    clarification_question = ClarificationGenerator.generate_question(
                        validation_result["missing_fields"]
                    )

                    ConversationStateManager.save_workflow(
                        session_id=session_id,
                        workflow_data={
                            "intent": intent,
                            "slots": slots,
                            "missing_fields": validation_result["missing_fields"]
                        }
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

        response["confirmation_summary"] = ConfirmationPresenter.build_transaction_confirmation(
            slots=slots
        )

        return response
    
    async def handle_clarification(self, session_id, message, pending_workflow):
        slots = pending_workflow["slots"]
        missing_fields = pending_workflow["missing_fields"]

        pending_suggestion = pending_workflow.get("pending_suggestion")
        if pending_suggestion:
            normalized_message = message.strip().lower()
            if normalized_message in ["yes", "yeah", "yup", "y"]:
                field = pending_suggestion["field"]
                suggested_value = pending_suggestion["value"]
                slots[field] = suggested_value
                if field == "account":
                    resolved_account = self.account_resolver.resolve(suggested_value)
                    slots["account_id"] = resolved_account.id
                
                ConversationStateManager.clear_workflow(session_id=session_id)

                return {
                    "success": True,
                    "intent":pending_workflow["intent"],
                    "slots": slots,
                    "requires_confirmation": True
                }
            
            if normalized_message in ["no", "nope", "nah", "n"]:
                ConversationStateManager.save_workflow(
                    session_id=session_id,
                    workflow_data={
                        "intent": pending_workflow["intent"],
                        "slots": slots,
                        "missing_fields": missing_fields
                    }
                )

                return {
                    "success": False,
                    "intent": pending_workflow["intent"],
                    "slots": slots,
                    "requires_clarification": True,
                    "clarification_question": (
                        "Okay. Please provide the correct account."
                    )
                }

        first_missing_field = missing_fields[0]

        if first_missing_field == "account":
            is_valid = ClarificationValidator.validate_account(message)

            resolved_account = self.account_resolver.resolve(message)
            if not resolved_account:
                suggested_account = self.account_resolver.suggest_account(message)
                if suggested_account:
                    ConversationStateManager.save_workflow(
                        session_id=session_id,
                        workflow_data={
                            "intent": pending_workflow["intent"],
                            "slots": slots,
                            "missing_fields": missing_fields,
                            "pending_suggestion": {
                                "field": "account",
                                "value": suggested_account
                            }
                        }
                    )

                    return {
                        "success": False,
                        "intent": pending_workflow["intent"],
                        "slots": slots,
                        "requires_clarification": True,
                        "clarification_question": (
                            f"Did you mean '{suggested_account}'?"
                        )
                    }
            

            if not is_valid:
                account_service = AccountService(self.db)
                available_accounts = account_service.get_account_names()
                return {
                    "success": False,
                    "intent": pending_workflow["intent"],
                    "slots": slots,
                    "requires_clarification": True,
                    "clarification_question": (
                        "I could not understand or find that account.\n\n"
                        "Available accounts:\n"
                        f"{available_accounts}"
                    )
                }
            
        slots["account_id"] = resolved_account.id
        slots[first_missing_field] = message

        ConversationStateManager.clear_workflow(session_id=session_id)

        return {
            "success": True,
            "intent":pending_workflow["intent"],
            "slots": slots,
            "requires_confirmation": True
        }