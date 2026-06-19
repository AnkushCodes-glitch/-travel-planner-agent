import asyncio
from tavily import TavilyClient
from app.config import settings


tavily_client = TavilyClient(api_key=settings.TAVILY_API_KEY)


HOTEL_SEARCH_TOOL = {
    "type": "function",
    "function": {
        "name": "search_hotels",
        "description": "Search for available hotels in a specific location for given check-in and check-out dates. Use this when the user wants to find hotels, asks about accommodation, or mentions where they want to stay.",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city or area where the user wants to stay"
                },
                "check_in_date": {
                    "type": "string",
                    "description": "Check-in date in YYYY-MM-DD format"
                },
                "check_out_date": {
                    "type": "string",
                    "description": "Check-out date in YYYY-MM-DD format"
                }
            },
            "required": ["location", "check_in_date", "check_out_date"]
        }
    }
}


async def search_hotels(location: str, check_in_date: str, check_out_date: str) -> dict:
    query = f"hotels in {location} check-in {check_in_date} check-out {check_out_date} price per night"

    response = await asyncio.to_thread(
        tavily_client.search,
        query=query,
        max_results=5
    )

    hotels = []
    for result in response.get("results", []):
        hotels.append({
            "name": result.get("title", "Unknown Hotel"),
            "location": location,
            "check_in_date": check_in_date,
            "check_out_date": check_out_date,
            "price_per_night": "Check source",
            "rating": None,
            "source_url": result.get("url"),
            "snippet": result.get("content", "")[:200]
        })

    return {"hotels": hotels}