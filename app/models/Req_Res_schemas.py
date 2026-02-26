from pydantic import BaseModel
from typing import Dict,Optional

class ChatRequest(BaseModel):
    session_id: str
    user_message: str
    conversation_history: Optional[Dict] = None

class ChatResponse(BaseModel):
    natural_language_answer: str
    sql_query: str
    token_usage: Dict
    latency_ms: float
    provider: str
    model:str
    status: str