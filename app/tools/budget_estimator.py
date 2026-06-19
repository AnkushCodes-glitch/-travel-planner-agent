CALCULATE_BUDGET_TOOL = {
    "type": "function",
    "function": {
        "name": "calculate_budget",
        "description": "Calculate the total estimated cost of the trip based on flight cost, hotel cost, number of nights, and number of travelers. Use this after flights and hotels have been found, when the user asks about total cost or budget.",
        "parameters": {
            "type": "object",
            "properties": {
                "flight_cost_per_person": {
                    "type": "number",
                    "description": "Estimated flight cost per person in INR"
                },
                "hotel_cost_per_night": {
                    "type": "number",
                    "description": "Estimated hotel cost per night in INR"
                },
                "num_nights": {
                    "type": "integer",
                    "description": "Number of nights the user will stay"
                },
                "num_travelers": {
                    "type": "integer",
                    "description": "Number of people traveling"
                }
            },
            "required": ["flight_cost_per_person", "hotel_cost_per_night", "num_nights", "num_travelers"]
        }
    }
}


async def calculate_budget(
    flight_cost_per_person: float,
    hotel_cost_per_night: float,
    num_nights: int,
    num_travelers: int
) -> dict:
    flight_cost = flight_cost_per_person * num_travelers
    hotel_cost = hotel_cost_per_night * num_nights
    food_cost = num_nights * 1000 * num_travelers
    activities_cost = num_nights * 500 * num_travelers
    total_cost = flight_cost + hotel_cost + food_cost + activities_cost

    return {
        "budget": {
            "flight_cost": flight_cost,
            "hotel_cost": hotel_cost,
            "food_cost": food_cost,
            "activities_cost": activities_cost,
            "total_cost": total_cost,
            "currency": "INR"
        }
    }