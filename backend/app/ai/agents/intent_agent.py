class IntentAgent:

    def __init__(self, llm_provider):
        self.llm_provider = llm_provider

    async def detect(self, message: str):
        prompt = (
            f"Detect intent from: {message}"
        )

        response = await self.llm_provider.generate(prompt)

        return response["intent"]