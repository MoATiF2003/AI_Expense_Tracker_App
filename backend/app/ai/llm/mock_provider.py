from app.ai.llm.base_llm import BaseLLM

class MockProvider(BaseLLM):

    async def generate(self, prompt: str):

        prompt_lower = prompt.lower()

        if "detect intent" in prompt_lower:
            return {
                "intent": "create_transaction"
            }

        if "extract slots" in prompt_lower:
            return {
                "amount": 250,
                "category": "Food",
                "account": "Cash Wallet",
                "transaction_type": "expense",
                "description": "Lunch"
            }

        return {
            "message": "Unknown prompt" 
        }