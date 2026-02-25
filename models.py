from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum

class Status(str, Enum):
    """Status enum for API responses"""
    OK = "ok"
    ERROR = "error"

class ChatRequest(BaseModel):
    """
    Request model for chat endpoint
    This defines what the client must send
    """
    session_id: str = Field(..., description="Unique session identifier")
    message: str = Field(..., description="User's question")
    context: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional context")

class TokenUsage(BaseModel):
    """Token usage information from the LLM"""
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

class ChatResponse(BaseModel):
    """
    Response model for chat endpoint
    This defines what the API will return
    """
    natural_language_answer: str
    sql_query: str
    token_usage: TokenUsage
    latency_ms: int
    provider: str = "gemini"
    model: str
    status: Status