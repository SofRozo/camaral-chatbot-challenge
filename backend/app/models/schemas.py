from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ChatRequest(BaseModel):
    """Request model for chat messages."""
    message: str
    session_id: Optional[str] = "default"


class ChatResponse(BaseModel):
    """Response model for chat messages."""
    content: str
    agent_used: str
    confidence: float
    suggestions: list[str] = []
    timestamp: datetime = datetime.utcnow()


class Message(BaseModel):
    """Single message in conversation."""
    role: str  # "user" or "assistant"
    content: str
    timestamp: datetime = datetime.utcnow()


class ConversationHistory(BaseModel):
    """Conversation history for a session."""
    session_id: str
    messages: list[dict] = []
    created_at: datetime = datetime.utcnow()


class AgentResponse(BaseModel):
    """Internal response from an agent."""
    content: str
    confidence: float
    sources: list[str] = []
