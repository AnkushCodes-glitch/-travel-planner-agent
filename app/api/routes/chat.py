from fastapi import APIRouter, HTTPException
from app.models.chat import ChatRequest, ChatResponse, TripContext
from app.services.chat_service import process_chat

# ApiRouter creates a mini-app for chat routes
# ALL routes defined here will be prefixed with /api/chat (set in main.py )
router = APIRouter()



@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main chat endpoint - Divesh calls this from React frontend.
    
    Receives: session_id + user message
    Returns: AI reply + structured travel data + trip context
    """
    try:
        # Pass session_id and message to chat service
        # Chat service handles memory, orchestrator, and tool calling
        result = await process_chat(
            session_id=request.session_id,
            user_message=request.message
        )

        # Build and return the structured response
        # This is the exact JSON shape Divesh's frontend receives
        return ChatResponse(
            session_id=request.session_id,
            reply=result["reply"],
            data=result["data"],
            trip_context=result["trip_context"]
        )

    except Exception as e:
        # If anything goes wrong, return a clean error
        # Never expose raw Python errors to the frontend
        raise HTTPException(
            status_code=500,
            detail=f"Agent error: {str(e)}"
        )