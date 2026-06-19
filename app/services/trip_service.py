from app.db.mongodb import get_database
from app.models.trip import TripPlan

# This service handles all MongoDB operations for trips
# Routes call these functions — keeping database logic out of routes


async def save_trip(trip: TripPlan) -> str:
    """
    Save a trip plan to MongoDB.
    Returns the inserted document ID as a string.
    """
    db = get_database()

    # Convert Pydantic model to dict for MongoDB
    # model_dump() is Pydantic v2 way to convert model → dict
    # exclude_none=True removes fields that are None (cleaner documents)
    trip_dict = trip.model_dump(exclude_none=True)

    # Insert into 'trips' collection
    result = await db.trips.insert_one(trip_dict)

    # Return the MongoDB generated ID as string
    # MongoDB returns ObjectId, we convert to string for JSON response
    return str(result.inserted_id)


async def get_trips(session_id: str) -> list:
    """
    Retrieve all saved trips for a session from MongoDB.
    Returns a list of trip documents.
    """
    db = get_database()

    # Find all trips matching this session_id
    # to_list(100) means fetch maximum 100 documents
    trips = await db.trips.find(
        {"session_id": session_id}
    ).to_list(100)

    # MongoDB documents contain '_id' field (ObjectId type)
    # ObjectId is NOT JSON serializable — convert to string
    # Otherwise FastAPI will crash when trying to return the response
    for trip in trips:
        trip["_id"] = str(trip["_id"])

    return trips