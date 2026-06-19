import asyncio
from tavily import TavilyClient
from app.config import settings

tavily_client = TavilyClient(api_key=settings.TAVILY_API_KEY)


FLIGHT_SEARCH_TOOL = {
    "type": "function",
    "function": {
        "name": "search_flights",
        "description": "Search for available flights between two cities on a specific date. Use this when the user wants to find flights, asks about flight prices, or mentions traveling from one city to another.",
        "parameters": {
            "type": "object",
            "properties": {
                "departure_city": {
                    "type": "string",
                    "description": "The city the user is departing from"
                },
                "arrival_city": {
                    "type": "string",
                    "description": "The destination city"
                },
                "departure_date": {
                    "type": "string",
                    "description": "The date of travel in YYYY-MM-DD format"
                }
            },
            "required": ["departure_city", "arrival_city", "departure_date"]
        }
    }
}


async def search_flights(departure_city: str, arrival_city: str, departure_date: str) -> dict:
    query = f"flights from {departure_city} to {arrival_city} on {departure_date} price"

    response = await asyncio.to_thread(
        tavily_client.search,
        query=query,
        max_results=5
    )

    flights = []
    for result in response.get("results", []):
        flights.append({
            "airline": "See details",
            "departure_city": departure_city,
            "arrival_city": arrival_city,
            "departure_date": departure_date,
            "price": "Check source",
            "duration": None,
            "source_url": result.get("url"),
            "snippet": result.get("content", "")[:200]
        })

    return {"flights": flights}