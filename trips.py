from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.core.database import get_db
from app.models.models import Trip, TripStop
from app.schemas.schemas import TripCreate, TripOut, TripStopCreate, TripStopOut, RouteOptimizationRequest, RouteOptimizationResult
from app.services.graph_algorithms import optimize_multi_stop_route

router = APIRouter()


@router.post("/", response_model=TripOut, status_code=201)
async def create_trip(data: TripCreate, db: AsyncSession = Depends(get_db)):
    trip = Trip(**data.model_dump(), user_id=1)  # user_id from JWT in production
    db.add(trip)
    await db.commit()
    await db.refresh(trip)
    return trip


@router.get("/", response_model=List[TripOut])
async def list_trips(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Trip).order_by(Trip.created_at.desc()))
    return result.scalars().all()


@router.get("/{trip_id}", response_model=TripOut)
async def get_trip(trip_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Trip).where(Trip.id == trip_id))
    trip = result.scalar_one_or_none()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    return trip


@router.post("/{trip_id}/stops", response_model=TripStopOut, status_code=201)
async def add_stop(trip_id: int, data: TripStopCreate, db: AsyncSession = Depends(get_db)):
    # Get current stop count for ordering
    result = await db.execute(select(TripStop).where(TripStop.trip_id == trip_id))
    existing = result.scalars().all()
    stop = TripStop(**data.model_dump(), order_index=len(existing))
    db.add(stop)
    await db.commit()
    await db.refresh(stop)
    return stop


@router.get("/{trip_id}/stops", response_model=List[TripStopOut])
async def list_stops(trip_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(TripStop).where(TripStop.trip_id == trip_id).order_by(TripStop.order_index)
    )
    return result.scalars().all()


@router.post("/optimize", response_model=RouteOptimizationResult)
async def optimize_route(req: RouteOptimizationRequest, db: AsyncSession = Depends(get_db)):
    stops_result = await db.execute(
        select(TripStop).where(TripStop.trip_id == req.trip_id).order_by(TripStop.order_index)
    )
    stops = stops_result.scalars().all()

    if len(stops) < 2:
        raise HTTPException(status_code=400, detail="Need at least 2 stops to optimize")

    stop_dicts = [{"id": s.id, "lat": s.latitude, "lon": s.longitude, "name": s.name} for s in stops]
    result = optimize_multi_stop_route(stop_dicts, algorithm=req.algorithm, optimize_for=req.optimize_for)

    # Persist optimized route on trip
    trip_result = await db.execute(select(Trip).where(Trip.id == req.trip_id))
    trip = trip_result.scalar_one_or_none()
    if trip:
        trip.optimized_route = result
        await db.commit()

    stop_map = {s.id: s for s in stops}
    ordered_stops_out = [stop_map[sid] for sid in result["ordered_stop_ids"] if sid in stop_map]

    return RouteOptimizationResult(
        trip_id=req.trip_id,
        algorithm_used=req.algorithm,
        total_distance_km=result["total_distance_km"],
        total_travel_time_mins=result["total_travel_time_mins"],
        ordered_stops=ordered_stops_out,
        edges=result["edges"],
    )
