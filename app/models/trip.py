from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class Flight(BaseModel):
    airline: str
    departure_city: str
    arrival_city: str
    departure_date: str
    price: str
    duration: Optional[str] = None
    source_url: Optional[str] = None


class Hotel(BaseModel):
    name: str
    location: str
    price_per_night: str
    rating: Optional[str] = None
    source_url: Optional[str] = None


class Recommendation(BaseModel):
    name: str
    category: str  # "food", "attraction", "activity"
    description: str
    source_url: Optional[str] = None


class Budget(BaseModel):
    flight_cost: float
    hotel_cost: float
    food_cost: float
    activities_cost: float
    total_cost: float
    currency: str = "INR"


class TripPlan(BaseModel):
    session_id: str
    destination: str
    departure_city: str
    departure_date: Optional[str] = None
    return_date: Optional[str] = None
    num_travelers: int = 1
    flights: List[Flight] = []
    hotels: List[Hotel] = []
    recommendations: List[Recommendation] = []
    budget: Optional[Budget] = None
    created_at: datetime = datetime.utcnow()