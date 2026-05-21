from app.ai.llm.base_llm import BaseLLM

class MockProvider(BaseLLM):

    async def generate(self, prompt: str):

        prompt_lower = prompt.lower()

        if "intent classification system" in prompt_lower:
            return {
                "intent": "create_transaction"
            }

        if "extract slots" in prompt_lower:
            return {
                "amount": 250,
                "account": "Fed Account",
                "transaction_type": "expense",
                "description": "Netflix Subscription"
            }
        
        if "finance category resolution system" in prompt_lower:
            if "netflix" in prompt_lower:
                return {
                    "matched_category": "Entertainment",
                    "proposed_new_category": None
                }
            return {
                "matched_category": None,
                "proposed_new_category": "Subscription"
            }
        
        return {
            "message": "Unknown prompt" 
        }