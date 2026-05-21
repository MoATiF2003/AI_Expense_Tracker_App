from app.ai.prompts.slot_prompt import build_slot_prompt

class SlotAgent:

    def __init__(self, llm_provider):
        self.llm_provider = llm_provider

    async def extract(self, message: str):
        prompt = build_slot_prompt(message=message)

        response = await self.llm_provider.generate(prompt=prompt)

        return response