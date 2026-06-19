from fastapi import APIRouter, HTTPException
from app.services.trip_service import save_trip, get_trips
from app.models.trip import TripPlan

# Router for trip-related endpoints
# All routes here are prefixed with /api/trips (set in main.py)
router = APIRouter()


@router.post("/save")
async def save_trip_route(trip: TripPlan):
    """
    Save a finalized trip plan to MongoDB.
    Divesh calls this when user clicks 'Save Trip' in the frontend.
    """
    try:
        # Pass trip data to service layer
        # Service handles actual MongoDB operation
        result = await save_trip(trip)
        return {"message": "Trip saved successfully", "trip_id": result}

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save trip: {str(e)}"
        )


@router.get("/{session_id}")
async def get_trips_route(session_id: str):
    """
    Retrieve all saved trips for a session.
    Divesh calls this to show user their saved trips.
    """
    try:
        # Fetch trips from MongoDB via service layer
        trips = await get_trips(session_id)
        return {"trips": trips}

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve trips: {str(e)}"
        )