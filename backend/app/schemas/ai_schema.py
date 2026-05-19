from pydantic import BaseModel
from typing import Any, Optional

class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    success: bool

    intent: Optional[str] = None

    slots: Optional[dict[str, Any]] = None

    error: Optional[str] = None

    retry_required: Optional[bool] = None

    requires_confirmation: Optional[bool] = None
