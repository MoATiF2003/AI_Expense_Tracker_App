class ExpenseOrchestrator:

    def __init__(self, intent_agent, slot_agent):
        self.intent_agent = intent_agent
        self.slot_agent = slot_agent

    async def process_message(self, message: str):
        intent = await self.intent_agent.detect(message)
        slots = await self.slot_agent.extract(message)

        return {
            "intent": intent,
            "slots": slots
        }