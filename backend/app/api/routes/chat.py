from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from pydantic import BaseModel
from typing import Optional
import json

from app.agents.orchestrator import Orchestrator
from app.models.schemas import ChatRequest, ChatResponse, ConversationHistory

router = APIRouter()

# Store conversations in memory (use Redis in production)
conversations: dict[str, ConversationHistory] = {}

# Initialize orchestrator
orchestrator = Orchestrator()


class MessageRequest(BaseModel):
    message: str
    session_id: Optional[str] = "default"


@router.post("/message", response_model=ChatResponse)
async def send_message(request: MessageRequest):
    """Send a message and get a response from the multi-agent system."""
    try:
        # Get or create conversation history
        if request.session_id not in conversations:
            conversations[request.session_id] = ConversationHistory(
                session_id=request.session_id,
                messages=[]
            )
        
        history = conversations[request.session_id]
        
        # Process message through orchestrator
        response = await orchestrator.process(
            message=request.message,
            history=history.messages
        )
        
        # Update history
        history.messages.append({"role": "user", "content": request.message})
        history.messages.append({"role": "assistant", "content": response.content})
        
        # Keep only last 10 messages for context
        if len(history.messages) > 20:
            history.messages = history.messages[-20:]
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.websocket("/ws/{session_id}")
async def websocket_chat(websocket: WebSocket, session_id: str):
    """WebSocket endpoint for real-time chat."""
    await websocket.accept()
    
    # Initialize conversation history
    if session_id not in conversations:
        conversations[session_id] = ConversationHistory(
            session_id=session_id,
            messages=[]
        )
    
    try:
        while True:
            # Receive message
            data = await websocket.receive_text()
            message_data = json.loads(data)
            user_message = message_data.get("message", "")
            
            if not user_message:
                continue
            
            history = conversations[session_id]
            
            # Send typing indicator
            await websocket.send_json({
                "type": "typing",
                "content": True
            })
            
            # Process message
            response = await orchestrator.process(
                message=user_message,
                history=history.messages
            )
            
            # Update history
            history.messages.append({"role": "user", "content": user_message})
            history.messages.append({"role": "assistant", "content": response.content})
            
            # Send response
            await websocket.send_json({
                "type": "message",
                "content": response.content,
                "agent": response.agent_used,
                "suggestions": response.suggestions
            })
            
    except WebSocketDisconnect:
        print(f"Client {session_id} disconnected")


@router.delete("/session/{session_id}")
async def clear_session(session_id: str):
    """Clear conversation history for a session."""
    if session_id in conversations:
        del conversations[session_id]
    return {"status": "cleared", "session_id": session_id}
