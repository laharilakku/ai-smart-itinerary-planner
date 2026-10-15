from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime
from app.models.models import TripStatus


# ─── Auth ────────────────────────────────────────────────────────────────────
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    preferred_currency: str = "INR"


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserOut(BaseModel):
    id: int
    name: str
    email: str
    preferred_currency: str
    created_at: datetime
    class Config:
        from_attributes = True


# ─── Trip ─────────────────────────────────────────────────────────────────────
class TripCreate(BaseModel):
    title: str
    destination: str
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    total_budget: Optional[float] = 0.0
    currency: str = "INR"
    notes: Optional[str]


class TripOut(TripCreate):
    id: int
    user_id: int
    status: TripStatus
    optimized_route: Optional[Dict[str, Any]]
    created_at: datetime
    class Config:
        from_attributes = True


# ─── Attraction ───────────────────────────────────────────────────────────────
class AttractionCreate(BaseModel):
    name: str
    category: str
    latitude: float
    longitude: float
    city: str
    country: str
    rating: Optional[float] = 0.0
    visit_duration_hrs: Optional[float] = 1.0
    entry_fee: Optional[float] = 0.0
    description: Optional[str]
    tags: Optional[List[str]] = []


class AttractionOut(AttractionCreate):
    id: int
    cluster_id: Optional[int]
    class Config:
        from_attributes = True


# ─── Trip Stop ────────────────────────────────────────────────────────────────
class TripStopCreate(BaseModel):
    trip_id: int
    attraction_id: Optional[int]
    name: str
    latitude: float
    longitude: float
    notes: Optional[str]


class TripStopOut(TripStopCreate):
    id: int
    order_index: int
    arrival_time: Optional[datetime]
    travel_time_to_next_mins: Optional[float]
    distance_to_next_km: Optional[float]
    class Config:
        from_attributes = True


# ─── Route Optimization ───────────────────────────────────────────────────────
class RouteOptimizationRequest(BaseModel):
    trip_id: int
    algorithm: str = "dijkstra"   # "dijkstra" | "astar"
    optimize_for: str = "time"    # "time" | "distance"


class RouteOptimizationResult(BaseModel):
    trip_id: int
    algorithm_used: str
    total_distance_km: float
    total_travel_time_mins: float
    ordered_stops: List[TripStopOut]
    edges: List[Dict[str, Any]]


# ─── Recommendation ───────────────────────────────────────────────────────────
class RecommendationRequest(BaseModel):
    city: str
    categories: Optional[List[str]] = []
    top_n: int = 10


class RecommendationResult(BaseModel):
    attraction: AttractionOut
    similarity_score: float
    cluster_label: str


# ─── Expense ──────────────────────────────────────────────────────────────────
class ExpenseCreate(BaseModel):
    trip_id: int
    category: str
    description: str
    amount: float
    currency: str = "INR"


class ExpenseOut(ExpenseCreate):
    id: int
    amount_inr: Optional[float]
    date: datetime
    class Config:
        from_attributes = True


class ExpenseSummary(BaseModel):
    trip_id: int
    total_inr: float
    budget_inr: float
    remaining_inr: float
    by_category: Dict[str, float]
    currency_breakdown: Dict[str, float]
