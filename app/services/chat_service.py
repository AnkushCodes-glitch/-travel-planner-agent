from app.agents.orchestrator import run_orchestrator
from app.models.chat import TripContext

# In-memory session store
# Key = session_id, Value = conversation history
session_store: dict = {}


def get_session_messages(session_id: str) -> list:
    if session_id not in session_store:
        session_store[session_id] = []
    return session_store[session_id]


def clear_session(session_id: str):
    if session_id in session_store:
        del session_store[session_id]


async def process_chat(session_id: str, user_message: str) -> dict:
    # Step 1: Load existing conversation history
    messages = get_session_messages(session_id)

    # Step 2: Add user's new message
    messages.append({
        "role": "user",
        "content": user_message
    })

    # Step 3: Run orchestrator with full history
    result = await run_orchestrator(messages)

    # Step 4: Update session with new messages
    session_store[session_id] = result["messages"]

    # Step 5: Extract trip context from data
    data = result.get("data", {})
    flights = data.get("flights", [])
    hotels = data.get("hotels", [])

    trip_context = TripContext()
    if flights:
        trip_context.departure_city = flights[0].get("departure_city")
        trip_context.destination = flights[0].get("arrival_city")
        trip_context.departure_date = flights[0].get("departure_date")
    if hotels:
        trip_context.destination = hotels[0].get("location")
        trip_context.departure_date = hotels[0].get("check_in_date")
        trip_context.return_date = hotels[0].get("check_out_date")

    return {
        "reply": result["reply"],
        "data": data,
        "trip_context": trip_context
    }