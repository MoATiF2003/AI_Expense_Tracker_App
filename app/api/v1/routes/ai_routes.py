from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.ai.agents.intent_agent import IntentAgent
from app.ai.agents.slot_agent import SlotAgent
# from app.ai.llm.mock_provider import MockProvider
from app.ai.llm.groq_provider import GroqProvider
from app.ai.orchestrators.expense_orchestrator import ExpenseOrchestrator
from app.schemas.ai_schema import ChatRequest, ChatResponse
from app.core.database import get_db
from app.ai.services.ai_execution_service import AIExecutionService
from app.schemas.ai_schema import ExecuteAIActionRequest

router = APIRouter(
    prefix="/ai",
    tags=["AI"]
)

@router.post("/chat", response_model=ChatResponse)
async def chat_with_ai(request: ChatRequest, db: Session = Depends(get_db)):
    llm_provider = GroqProvider()
    
    intent_agent = IntentAgent(llm_provider)
    slot_agent = SlotAgent(llm_provider)

    orchestrator = ExpenseOrchestrator(intent_agent=intent_agent, slot_agent=slot_agent, db=db)

    result = await orchestrator.process_message(
        session_id=request.session_id, 
        message=request.message
    )

    return result

@router.post("/execute")
async def execute_ai_action(request: ExecuteAIActionRequest, db: Session = Depends(get_db)):
    execution_service = AIExecutionService(db=db)

    if request.intent == "create_transaction":
        transaction = execution_service.execute_transaction(
            slots=request.slots,
            proposed_new_category=request.proposed_new_category
        )

        return {
            "success": True,
            "transaction_id": transaction.id
        }
    
    return {
        "success": False,
        "error": "Unsupported intent"
    }