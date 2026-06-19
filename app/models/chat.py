from pydantic import BaseModel
from typing import Optional, List, Dict, Any


class ChatRequest(BaseModel):
    session_id: str
    message: str


class TripContext(BaseModel):
    destination: Optional[str] = None
    departure_city: Optional[str] = None
    departure_date: Optional[str] = None
    return_date: Optional[str] = None
    num_travelers: int = 1
    budget_range: Optional[str] = None


class ChatResponse(BaseModel):
    session_id: str
    reply: str
    data: Dict[str, Any] = {}
    trip_context: TripContext