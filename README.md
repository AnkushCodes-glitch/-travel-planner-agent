# Travel Planner Agent

An AI-powered travel planning agent built with FastAPI, Groq LLM, and Tavily Search.
The agent helps users find flights, hotels, local recommendations, and estimate trip budgets through a natural conversation.

## What It Does

- Searches real flights between cities
- Finds hotels at the destination
- Recommends local food and attractions
- Calculates total trip budget in INR
- Remembers conversation context across multiple messages

## Tech Stack

- **FastAPI** — REST API backend
- **Groq API** (llama-3.3-70b-versatile) — LLM with tool calling
- **Tavily Search** — Real-time web search for flights and hotels
- **MongoDB Atlas** — Stores saved trip plans
- **Motor** — Async MongoDB driver
- **Pydantic v2** — Data validation and models

## Architecture

User Message

↓

FastAPI Route

↓

Chat Service (session memory)

↓

Orchestrator (Groq LLM decides which tools to call)

↓

Tools run in parallel (asyncio.gather)

├── Flight Search (Tavily)

├── Hotel Search (Tavily)

├── Recommendations (Tavily)

└── Budget Calculator (pure logic)

↓

Structured JSON Response

## API Endpoints

| Method | Endpoint                  | Description                        |
| ------ | ------------------------- | ---------------------------------- |
| POST   | `/api/chat/`              | Send a message to the travel agent |
| POST   | `/api/trips/save`         | Save a finalized trip to MongoDB   |
| GET    | `/api/trips/{session_id}` | Get saved trips for a session      |

## Request/Response Example

**Request:**

```json
{
  "session_id": "user-123",
  "message": "Find flights from Mumbai to Goa on 2025-07-15"
}
```

**Response:**

```json
{
  "session_id": "user-123",
  "reply": "I found flights from Mumbai to Goa starting at ₹4248...",
  "data": {
    "flights": [...],
    "hotels": [...],
    "recommendations": [...],
    "budget": {...}
  },
  "trip_context": {
    "destination": "Goa",
    "departure_city": "Mumbai",
    "departure_date": "2025-07-15"
  }
}
```

## Setup & Installation

1. Clone the repository

```bash
git clone https://github.com/AnkushCodes-glitch/-travel-planner-agent.git
cd travel-planner-agent
```

2. Create virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Create `.env` file
   GROQ_API_KEY=your_groq_key

TAVILY_API_KEY=your_tavily_key

MONGODB_URI=your_mongodb_uri

DATABASE_NAME=travel_agent

5. Run the server

```bash
uvicorn app.main:app --reload
```

6. Visit `http://127.0.0.1:8000/docs` for interactive API documentation

## Project Structure

app/

├── main.py # FastAPI app entry point

├── config.py # Environment variables

├── agents/

│ └── orchestrator.py # LLM brain - tool calling loop

├── tools/

│ ├── flight_search.py

│ ├── hotel_search.py

│ ├── recommendations.py

│ └── budget_estimator.py

├── services/

│ ├── chat_service.py # Session memory management

│ └── trip_service.py # MongoDB operations

├── models/

│ ├── chat.py # Request/Response models

│ └── trip.py # Trip data models

├── api/routes/

│ ├── chat.py # Chat endpoints

│ └── trips.py # Trip endpoints

└── db/

└── mongodb.py # Database connection

## Built By

Ankush — AI Engineer in training, Mumbai
Part of a structured Agentic AI learning roadmap.

Projects completed:

- Project 1: Lighting Business Agent
- Project 2: Mercedes Car Dealership Agent
- Project 3: Smart Shopping Price Arbitrage Agent
- Project 4: Travel Planner Agent (this project)
