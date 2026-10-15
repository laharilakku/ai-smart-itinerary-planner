from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.core.database import get_db
from app.models.models import Attraction
from app.schemas.schemas import RecommendationRequest, RecommendationResult
from app.services.recommendation_engine import (
    get_recommendations, cluster_attractions, build_feature_vector, get_cluster_label
)

router = APIRouter()


@router.post("/", response_model=List[RecommendationResult])
async def recommend_attractions(req: RecommendationRequest, db: AsyncSession = Depends(get_db)):
    """Get recommendations based on city and preferred categories."""
    query = select(Attraction).where(Attraction.city.ilike(f"%{req.city}%"))
    result = await db.execute(query)
    attractions = result.scalars().all()

    if not attractions:
        raise HTTPException(status_code=404, detail=f"No attractions found in {req.city}")

    att_dicts = [
        {
            "id": a.id, "name": a.name, "category": a.category,
            "tags": a.tags or [], "rating": a.rating,
            "visit_duration_hrs": a.visit_duration_hrs,
            "entry_fee": a.entry_fee, "city": a.city,
            "latitude": a.latitude, "longitude": a.longitude,
            "feature_vector": a.feature_vector, "cluster_id": a.cluster_id,
        }
        for a in attractions
    ]

    # Build query vector from categories
    query_dict = {
        "tags": req.categories or [],
        "rating": 4.0,
        "visit_duration_hrs": 2.0,
        "entry_fee": 0.0,
    }
    query_dict["feature_vector"] = build_feature_vector(query_dict)

    recs = get_recommendations(query_dict, att_dicts, top_n=req.top_n)
    return [
        RecommendationResult(
            attraction=r["attraction"],
            similarity_score=r["similarity_score"],
            cluster_label=r["cluster_label"],
        )
        for r in recs
    ]


@router.post("/cluster")
async def cluster_city_attractions(city: str, db: AsyncSession = Depends(get_db)):
    """Apply K-Means clustering to all attractions in a city."""
    result = await db.execute(select(Attraction).where(Attraction.city.ilike(f"%{city}%")))
    attractions = result.scalars().all()

    if not attractions:
        raise HTTPException(status_code=404, detail=f"No attractions found in {city}")

    att_dicts = [
        {
            "id": a.id, "name": a.name, "tags": a.tags or [],
            "rating": a.rating, "visit_duration_hrs": a.visit_duration_hrs,
            "entry_fee": a.entry_fee, "feature_vector": a.feature_vector,
        }
        for a in attractions
    ]

    clustered = cluster_attractions(att_dicts)

    # Persist cluster IDs back to DB
    for c in clustered:
        att_obj = next((a for a in attractions if a.id == c["id"]), None)
        if att_obj:
            att_obj.cluster_id = c["cluster_id"]
            att_obj.feature_vector = c["feature_vector"]
    await db.commit()

    summary = {}
    for c in clustered:
        label = get_cluster_label(c["cluster_id"])
        summary.setdefault(label, []).append(c["name"])

    return {"city": city, "clusters": summary}
