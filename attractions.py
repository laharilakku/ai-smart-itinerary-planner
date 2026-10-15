from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from app.core.database import get_db
from app.models.models import Attraction
from app.schemas.schemas import AttractionCreate, AttractionOut
from app.services.recommendation_engine import build_feature_vector

router = APIRouter()


@router.post("/", response_model=AttractionOut, status_code=201)
async def add_attraction(data: AttractionCreate, db: AsyncSession = Depends(get_db)):
    attraction = Attraction(
        **data.model_dump(),
        feature_vector=build_feature_vector(data.model_dump()),
    )
    db.add(attraction)
    await db.commit()
    await db.refresh(attraction)
    return attraction


@router.get("/", response_model=List[AttractionOut])
async def list_attractions(city: Optional[str] = None, category: Optional[str] = None, db: AsyncSession = Depends(get_db)):
    query = select(Attraction)
    if city:
        query = query.where(Attraction.city.ilike(f"%{city}%"))
    if category:
        query = query.where(Attraction.category == category)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{attraction_id}", response_model=AttractionOut)
async def get_attraction(attraction_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Attraction).where(Attraction.id == attraction_id))
    att = result.scalar_one_or_none()
    if not att:
        raise HTTPException(status_code=404, detail="Attraction not found")
    return att


@router.delete("/{attraction_id}", status_code=204)
async def delete_attraction(attraction_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Attraction).where(Attraction.id == attraction_id))
    att = result.scalar_one_or_none()
    if not att:
        raise HTTPException(status_code=404, detail="Attraction not found")
    await db.delete(att)
    await db.commit()
