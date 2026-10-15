"""
Attraction Recommendation Engine
- Content-based filtering with cosine similarity
- K-Means clustering to group nearby/similar attractions
"""

import numpy as np
import pickle
import os
from typing import List, Dict, Optional
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity


CATEGORIES = [
    "museum", "park", "beach", "temple", "fort",
    "restaurant", "market", "viewpoint", "adventure", "heritage",
]

CLUSTER_LABELS = {
    0: "Cultural & Heritage",
    1: "Nature & Outdoors",
    2: "Food & Markets",
    3: "Adventure & Sports",
    4: "Relaxation & Scenic",
}


def build_feature_vector(attraction: Dict) -> List[float]:
    """
    Build a numeric feature vector for an attraction.
    Features: one-hot categories, rating, duration, entry_fee (normalized)
    """
    cat_vector = [1.0 if c in (attraction.get("tags") or []) else 0.0 for c in CATEGORIES]
    rating = (attraction.get("rating") or 0.0) / 5.0
    duration = min((attraction.get("visit_duration_hrs") or 1.0) / 8.0, 1.0)
    fee = min((attraction.get("entry_fee") or 0.0) / 1000.0, 1.0)

    return cat_vector + [rating, duration, fee]


def compute_cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    a = np.array(vec_a).reshape(1, -1)
    b = np.array(vec_b).reshape(1, -1)
    return float(cosine_similarity(a, b)[0][0])


def get_recommendations(
    query_attraction: Dict,
    all_attractions: List[Dict],
    top_n: int = 10,
    city_filter: Optional[str] = None,
) -> List[Dict]:
    """
    Return top-N attractions most similar to query_attraction using cosine similarity.
    """
    query_vec = (
        query_attraction.get("feature_vector")
        or build_feature_vector(query_attraction)
    )

    scored = []
    for att in all_attractions:
        if att["id"] == query_attraction.get("id"):
            continue
        if city_filter and att.get("city", "").lower() != city_filter.lower():
            continue

        att_vec = att.get("feature_vector") or build_feature_vector(att)
        score = compute_cosine_similarity(query_vec, att_vec)
        scored.append((score, att))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [
        {
            "attraction": item,
            "similarity_score": round(score, 4),
            "cluster_label": CLUSTER_LABELS.get(item.get("cluster_id", 0), "General"),
        }
        for score, item in scored[:top_n]
    ]


def cluster_attractions(attractions: List[Dict], n_clusters: int = 5) -> List[Dict]:
    """
    Apply K-Means clustering to group attractions by feature similarity.
    Returns attractions with cluster_id assigned.
    """
    if len(attractions) < n_clusters:
        for att in attractions:
            att["cluster_id"] = 0
        return attractions

    vectors = [
        att.get("feature_vector") or build_feature_vector(att)
        for att in attractions
    ]
    X = np.array(vectors)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    labels = kmeans.fit_predict(X_scaled)

    for att, label in zip(attractions, labels):
        att["cluster_id"] = int(label)
        att["feature_vector"] = (att.get("feature_vector") or build_feature_vector(att))

    return attractions


def get_cluster_label(cluster_id: int) -> str:
    return CLUSTER_LABELS.get(cluster_id, "General")
