from app.ai.prompts.intent_prompt import build_intent_prompt

class IntentAgent:

    VALID_INTENTS = [
        "create_transaction",
        "get_transactions",
        "create_account",
        "create_category"
    ]

    def __init__(self, llm_provider):
        self.llm_provider = llm_provider

    async def detect(self, message: str):
        prompt = build_intent_prompt(message=message)

        response = await self.llm_provider.generate(prompt=prompt)

        return response["intent"]