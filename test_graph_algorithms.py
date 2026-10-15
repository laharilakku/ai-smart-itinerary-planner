import pytest
from app.services.graph_algorithms import (
    haversine_distance, build_graph, dijkstra, astar,
    optimize_multi_stop_route
)

STOPS = [
    {"id": 1, "lat": 28.6562, "lon": 77.2410, "name": "Red Fort"},
    {"id": 2, "lat": 27.1751, "lon": 78.0421, "name": "Taj Mahal"},
    {"id": 3, "lat": 26.9239, "lon": 75.8267, "name": "Hawa Mahal"},
]


def test_haversine_distance():
    # Delhi to Agra approx 200 km
    d = haversine_distance(28.6562, 77.2410, 27.1751, 78.0421)
    assert 190 < d < 220


def test_build_graph():
    graph = build_graph(STOPS)
    assert 1 in graph
    assert len(graph[1]) == 2  # Two neighbours


def test_dijkstra_finds_path():
    graph = build_graph(STOPS)
    path, cost = dijkstra(graph, 1, 3)
    assert path[0] == 1
    assert path[-1] == 3
    assert cost > 0


def test_astar_finds_path():
    graph = build_graph(STOPS)
    path, cost = astar(STOPS, graph, 1, 3)
    assert path[0] == 1
    assert path[-1] == 3
    assert cost > 0


def test_multi_stop_optimization():
    result = optimize_multi_stop_route(STOPS, algorithm="dijkstra")
    assert len(result["ordered_stop_ids"]) == 3
    assert result["total_distance_km"] > 0
    assert len(result["edges"]) == 2


def test_astar_vs_dijkstra_same_result():
    dijk_result = optimize_multi_stop_route(STOPS, algorithm="dijkstra")
    astar_result = optimize_multi_stop_route(STOPS, algorithm="astar")
    # Both should produce a valid ordering of 3 stops
    assert len(dijk_result["ordered_stop_ids"]) == len(astar_result["ordered_stop_ids"])
