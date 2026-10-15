from sqlalchemy import (
    Column, Integer, String, Float, DateTime, Boolean,
    ForeignKey, Text, JSON, Enum
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class TripStatus(str, enum.Enum):
    DRAFT = "draft"
    PLANNED = "planned"
    ONGOING = "ongoing"
    COMPLETED = "completed"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    preferred_currency = Column(String(10), default="INR")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    trips = relationship("Trip", back_populates="user")


class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(200), nullable=False)
    destination = Column(String(200), nullable=False)
    start_date = Column(DateTime(timezone=True))
    end_date = Column(DateTime(timezone=True))
    status = Column(Enum(TripStatus), default=TripStatus.DRAFT)
    total_budget = Column(Float, default=0.0)
    currency = Column(String(10), default="INR")
    notes = Column(Text, nullable=True)
    optimized_route = Column(JSON, nullable=True)   # Stores Dijkstra/A* result
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="trips")
    stops = relationship("TripStop", back_populates="trip", order_by="TripStop.order_index")
    expenses = relationship("Expense", back_populates="trip")


class Attraction(Base):
    __tablename__ = "attractions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    category = Column(String(100))          # museum, park, restaurant, etc.
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    city = Column(String(100))
    country = Column(String(100))
    rating = Column(Float, default=0.0)
    visit_duration_hrs = Column(Float, default=1.0)
    entry_fee = Column(Float, default=0.0)
    description = Column(Text, nullable=True)
    tags = Column(JSON, default=list)       # ["heritage", "outdoor", "family-friendly"]
    feature_vector = Column(JSON, nullable=True)  # For cosine similarity
    cluster_id = Column(Integer, nullable=True)   # K-Means cluster
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    trip_stops = relationship("TripStop", back_populates="attraction")


class TripStop(Base):
    __tablename__ = "trip_stops"

    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey("trips.id"), nullable=False)
    attraction_id = Column(Integer, ForeignKey("attractions.id"), nullable=True)
    order_index = Column(Integer, default=0)
    name = Column(String(200))              # Custom stop name if no attraction
    latitude = Column(Float)
    longitude = Column(Float)
    arrival_time = Column(DateTime(timezone=True), nullable=True)
    departure_time = Column(DateTime(timezone=True), nullable=True)
    travel_time_to_next_mins = Column(Float, nullable=True)
    distance_to_next_km = Column(Float, nullable=True)
    notes = Column(Text, nullable=True)

    trip = relationship("Trip", back_populates="stops")
    attraction = relationship("Attraction", back_populates="trip_stops")


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey("trips.id"), nullable=False)
    category = Column(String(100))          # transport, food, accommodation, entry
    description = Column(String(300))
    amount = Column(Float, nullable=False)
    currency = Column(String(10), default="INR")
    amount_inr = Column(Float, nullable=True)  # Converted to base currency
    date = Column(DateTime(timezone=True), server_default=func.now())

    trip = relationship("Trip", back_populates="expenses")
