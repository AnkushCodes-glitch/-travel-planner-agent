import asyncio
from tavily import TavilyClient
from app.config import settings


tavily_client = TavilyClient(api_key=settings.TAVILY_API_KEY)


GET_RECOMMENDATIONS_TOOL = {
    "type": "function",
    "function": {
        "name": "get_recommendations",
        "description": "Get local recommendations for food, attractions, and activities in a destination city. Use this when the user asks what to do, where to eat, or what to see at their destination.",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city to get recommendations for"
                },
                "category": {
                    "type": "string",
                    "enum": ["food", "attractions", "activities", "all"],
                    "description": "The type of recommendation requested. Use 'all' if the user wants a general overview."
                }
            },
            "required": ["location", "category"]
        }
    }
}


async def get_recommendations(location: str, category: str) -> dict:
    query = f"best {category} in {location}"

    response = await asyncio.to_thread(
        tavily_client.search,
        query=query,
        max_results=5
    )

    recommendations = []
    for result in response.get("results", []):
        recommendations.append({
            "name": result.get("title", "Unknown"),
            "category": category,
            "description": result.get("content", "")[:200],
            "source_url": result.get("url")
        })

    return {"recommendations": recommendations}