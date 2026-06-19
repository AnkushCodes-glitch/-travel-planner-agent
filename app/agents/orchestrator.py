import json
import asyncio
from groq import AsyncGroq
from app.config import settings
from app.tools.flight_search import FLIGHT_SEARCH_TOOL, search_flights
from app.tools.hotel_search import HOTEL_SEARCH_TOOL, search_hotels
from app.tools.recommendations import GET_RECOMMENDATIONS_TOOL, get_recommendations
from app.tools.budget_estimator import CALCULATE_BUDGET_TOOL, calculate_budget

# AsyncGroq is the async version of Groq client
# Same reason we use AsyncOpenAI - our FastAPI app is async
client = AsyncGroq(api_key=settings.GROQ_API_KEY)

# All tool definitions in one list - sent to LLM so it knows what tools exist
TOOLS = [
    FLIGHT_SEARCH_TOOL,
    HOTEL_SEARCH_TOOL,
    GET_RECOMMENDATIONS_TOOL,
    CALCULATE_BUDGET_TOOL
]

# Maps tool name (string) → actual Python function
# When LLM says "call search_flights", we look it up here
TOOL_MAP = {
    "search_flights": search_flights,
    "search_hotels": search_hotels,
    "get_recommendations": get_recommendations,
    "calculate_budget": calculate_budget
}

# System prompt - tells LLM who it is and how to behave
SYSTEM_PROMPT = """You are an expert travel planning assistant for Indian travelers.
You help users find flights, hotels, local recommendations, and estimate trip budgets.

Rules:
- Always extract destination, travel dates, and number of travelers from the conversation
- Search for flights and hotels when the user mentions travel plans
- Provide budget estimates after finding flights and hotels
- Give local food and activity recommendations for the destination
- Be helpful, concise, and specific
- Always mention prices in INR
- If information is missing (like travel dates), ask the user before calling tools
"""


async def run_orchestrator(messages: list) -> dict:
    collected_data = {}

    # Step 1: Send messages to Groq with tool definitions
    response = await client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": SYSTEM_PROMPT}] + messages,
        tools=TOOLS,
        tool_choice="auto"
    )

    response_message = response.choices[0].message

    # Step 2: Loop until LLM stops requesting tool calls
    while response_message.tool_calls:

        # Append raw response object directly
        # Groq reads its own response object correctly
        # Manually rebuilding the dict causes format errors
        messages.append(response_message)

        # Step 3: Build list of tool tasks to run in parallel
        tool_tasks = []
        for tool_call in response_message.tool_calls:
            tool_name = tool_call.function.name
            # json.loads converts argument string → Python dict
            tool_args = json.loads(tool_call.function.arguments)
            tool_func = TOOL_MAP.get(tool_name)

            if tool_func:
                tool_tasks.append((tool_call.id, tool_name, tool_func(**tool_args)))

        # Run all tools simultaneously instead of one by one
        # asyncio.gather is why we made all tool functions async
        results = await asyncio.gather(*[task[2] for task in tool_tasks])

        # Step 4: Add tool results to messages and collect data
        for i, (tool_call_id, tool_name, _) in enumerate(tool_tasks):
            result = results[i]
            # Merge each tool result into collected_data
            collected_data.update(result)

            # Send result back to LLM in correct format
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call_id,
                "content": json.dumps(result)
            })

        # Step 5: Send updated messages back to LLM for next decision
        response = await client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": SYSTEM_PROMPT}] + messages,
            tools=TOOLS,
            tool_choice="auto"
        )

        response_message = response.choices[0].message

    # Step 6: LLM has no more tool calls - return final reply
    final_reply = response_message.content or "I couldn't process your request. Please try again."

    # Add final reply to messages for session memory
    messages.append({
        "role": "assistant",
        "content": final_reply
    })

    return {
        "reply": final_reply,
        "data": collected_data,
        "messages": messages
    }