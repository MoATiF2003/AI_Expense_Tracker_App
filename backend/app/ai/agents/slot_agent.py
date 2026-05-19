class SlotAgent:

    def __init__(self, llm_provider):
        self.llm_provider = llm_provider

    async def extract(self, message: str):
        prompt = (
            f"Extract slots from: {message}"
        )

        response = await self.llm_provider.generate(prompt)

        return response