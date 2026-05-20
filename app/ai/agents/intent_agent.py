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
        prompt = f"""
You are an intent classification system.

You must return ONLY one of these intents:
{self.VALID_INTENTS}

Do not explain.
Do not add extra text.
Return ONLY the intent string.

User Message:
{message}
"""

        response = await self.llm_provider.generate(prompt)

        return response["intent"]