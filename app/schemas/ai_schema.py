from pydantic import BaseModel
from typing import Any, Optional

class ProposedNewCategorySchema(BaseModel):
    name: str

    type: str

class ChatRequest(BaseModel):
    session_id: str

    message: str


class ChatResponse(BaseModel):
    success: bool

    intent: Optional[str] = None

    slots: Optional[dict[str, Any]] = None

    error: Optional[str] = None

    retry_required: Optional[bool] = None

    requires_confirmation: Optional[bool] = None

    proposed_new_category: Optional[ProposedNewCategorySchema] = None

    missing_fields: Optional[list[str]] = None

    clarification_question: Optional[str] = None

    requires_clarification: Optional[bool] = None

    confirmation_summary: Optional[dict[str, Any]] = None

class ExecuteAIActionRequest(BaseModel):
    intent: str

    slots: dict[str, Any]

    proposed_new_category: Optional[ProposedNewCategorySchema] = None