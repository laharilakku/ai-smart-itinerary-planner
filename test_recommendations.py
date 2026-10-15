import pytest
from app.services.recommendation_engine import (
    build_feature_vector, compute_cosine_similarity,
    get_recommendations, cluster_attractions
)

SAMPLE_ATTRACTIONS = [
    {"id": 1, "name": "Red Fort", "tags": ["heritage", "history"], "rating": 4.5, "visit_duration_hrs": 2.0, "entry_fee": 35.0, "city": "Delhi"},
    {"id": 2, "name": "India Gate", "tags": ["monument", "park"], "rating": 4.4, "visit_duration_hrs": 1.0, "entry_fee": 0.0, "city": "Delhi"},
    {"id": 3, "name": "Taj Mahal", "tags": ["heritage", "UNESCO", "romantic"], "rating": 4.9, "visit_duration_hrs": 3.0, "entry_fee": 50.0, "city": "Agra"},
    {"id": 4, "name": "Amber Fort", "tags": ["fort", "heritage", "adventure"], "rating": 4.7, "visit_duration_hrs": 3.0, "entry_fee": 100.0, "city": "Jaipur"},
    {"id": 5, "name": "Marine Drive", "tags": ["viewpoint", "waterfront", "walk"], "rating": 4.5, "visit_duration_hrs": 1.5, "entry_fee": 0.0, "city": "Mumbai"},
]


def test_feature_vector_length():
    vec = build_feature_vector(SAMPLE_ATTRACTIONS[0])
    assert len(vec) == 13  # 10 categories + 3 numeric features


def test_cosine_similarity_self():
    vec = build_feature_vector(SAMPLE_ATTRACTIONS[0])
    assert compute_cosine_similarity(vec, vec) == pytest.approx(1.0, abs=0.01)


def test_cosine_similarity_different():
    vec_a = build_feature_vector(SAMPLE_ATTRACTIONS[0])  # heritage
    vec_b = build_feature_vector(SAMPLE_ATTRACTIONS[4])  # viewpoint
    sim = compute_cosine_similarity(vec_a, vec_b)
    assert 0.0 <= sim <= 1.0


def test_recommendations_returns_top_n():
    query = {"tags": ["heritage"], "rating": 4.5, "visit_duration_hrs": 2.0, "entry_fee": 30.0}
    recs = get_recommendations(query, SAMPLE_ATTRACTIONS, top_n=3)
    assert len(recs) <= 3


def test_cluster_attractions():
    clustered = cluster_attractions(SAMPLE_ATTRACTIONS, n_clusters=2)
    assert all("cluster_id" in a for a in clustered)
    assert all(a["cluster_id"] in [0, 1] for a in clustered)
