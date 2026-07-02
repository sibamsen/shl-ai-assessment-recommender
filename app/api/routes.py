"""
FastAPI route handlers for /health and /chat.
"""

from typing import List
from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel, Field

router = APIRouter()


# Request / Response Schemas
class Message(BaseModel):
    role: str = Field(..., description="Role of the sender: 'user' or 'assistant'")
    content: str = Field(..., description="Content of the message")


class ChatRequest(BaseModel):
    messages: List[Message] = Field(..., description="History of the conversation")


class Recommendation(BaseModel):
    name: str = Field(..., description="Exact name of the assessment")
    url: str = Field(..., description="Link to the assessment in the catalog")
    test_type: str = Field(..., description="Comma-separated test type code(s), e.g. 'P', 'K, S'")


class ChatResponse(BaseModel):
    reply: str = Field(..., description="Conversational text response")
    recommendations: List[Recommendation] = Field(..., description="Structured shortlist of recommendations")
    end_of_conversation: bool = Field(..., description="True if the conversation is completed")


# GET /health
@router.get("/health")
def health_check():
    return {"status": "ok"}


# POST /chat
@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, req: Request):
    manager = getattr(req.app.state, "manager", None)
    if not manager:
        raise HTTPException(status_code=500, detail="ConversationManager is not initialized.")
        
    try:
        # Convert request models to plain dictionaries
        history = [{"role": msg.role, "content": msg.content} for msg in request.messages]
        
        # Process using the ConversationManager
        response = manager.process_chat(history)
        
        return ChatResponse(
            reply=response["reply"],
            recommendations=[
                Recommendation(
                    name=rec["name"],
                    url=rec["url"],
                    test_type=rec["test_type"]
                )
                for rec in response["recommendations"]
            ],
            end_of_conversation=response["end_of_conversation"]
        )
    except Exception as e:
        # Log error locally
        print(f"Error in /chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))
