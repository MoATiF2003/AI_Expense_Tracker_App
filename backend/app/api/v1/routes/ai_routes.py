from fastapi import APIRouter

from app.ai.agents.intent_agent import IntentAgent
from app.ai.agents.slot_agent import SlotAgent
from app.ai.llm.mock_provider import MockProvider
from app.ai.orchestrators.expense_orchestrator import ExpenseOrchestrator
from app.schemas.ai_schema import ChatRequest, ChatResponse

router = APIRouter(
    prefix="/ai",
    tags=["AI"]
)

@router.post("/chat", response_model=ChatResponse)
async def chat_with_ai(request: ChatRequest):
    llm_provider = MockProvider()
    
    intent_agent = IntentAgent(llm_provider)
    slot_agent = SlotAgent(llm_provider)

    orchestrator = ExpenseOrchestrator(intent_agent=intent_agent, slot_agent=slot_agent)

    result = await orchestrator.process_message(request.message)

    return result