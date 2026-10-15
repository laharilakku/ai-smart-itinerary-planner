"""
Route optimization using Dijkstra's Algorithm and A* Search.
Stops are nodes; edge weights = travel time (minutes) or distance (km).
"""

import heapq
import math
from typing import List, Dict, Tuple, Optional


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Compute great-circle distance in km between two GPS coordinates.
    Used as the heuristic function in A* Search.
    """
    R = 6371.0  # Earth radius in km
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def estimate_travel_time_mins(distance_km: float, speed_kmh: float = 40.0) -> float:
    """Estimate travel time given distance and average city speed."""
    return (distance_km / speed_kmh) * 60


def build_graph(stops: List[Dict]) -> Dict[int, List[Tuple[int, float, float]]]:
    """
    Build a fully-connected weighted graph from a list of stops.
    Each stop: {"id": int, "lat": float, "lon": float}
    Returns: adjacency list { node_id: [(neighbor_id, time_mins, dist_km), ...] }
    """
    graph: Dict[int, List[Tuple[int, float, float]]] = {s["id"]: [] for s in stops}

    for i, src in enumerate(stops):
        for j, dst in enumerate(stops):
            if i == j:
                continue
            dist = haversine_distance(src["lat"], src["lon"], dst["lat"], dst["lon"])
            time = estimate_travel_time_mins(dist)
            graph[src["id"]].append((dst["id"], time, dist))

    return graph


def dijkstra(
    graph: Dict[int, List[Tuple[int, float, float]]],
    start: int,
    end: int,
    optimize_for: str = "time",
) -> Tuple[List[int], float]:
    """
    Dijkstra's shortest-path algorithm.
    optimize_for: "time" (index 0) | "distance" (index 1)
    Returns: (path as list of node ids, total cost)
    """
    weight_idx = 0 if optimize_for == "time" else 1

    dist = {node: float("inf") for node in graph}
    dist[start] = 0.0
    prev: Dict[int, Optional[int]] = {node: None for node in graph}
    pq = [(0.0, start)]

    while pq:
        cost, u = heapq.heappop(pq)
        if cost > dist[u]:
            continue
        for v, time_w, dist_w in graph[u]:
            w = time_w if weight_idx == 0 else dist_w
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                prev[v] = u
                heapq.heappush(pq, (dist[v], v))

    # Reconstruct path
    path, node = [], end
    while node is not None:
        path.append(node)
        node = prev[node]
    path.reverse()

    return path, dist[end]


def astar(
    stops: List[Dict],
    graph: Dict[int, List[Tuple[int, float, float]]],
    start: int,
    end: int,
    optimize_for: str = "time",
) -> Tuple[List[int], float]:
    """
    A* Search with haversine heuristic.
    optimize_for: "time" | "distance"
    """
    stop_map = {s["id"]: s for s in stops}
    goal_stop = stop_map[end]
    weight_idx = 0 if optimize_for == "time" else 1

    def heuristic(node_id: int) -> float:
        s = stop_map[node_id]
        d = haversine_distance(s["lat"], s["lon"], goal_stop["lat"], goal_stop["lon"])
        return estimate_travel_time_mins(d) if optimize_for == "time" else d

    g_cost = {node: float("inf") for node in graph}
    g_cost[start] = 0.0
    prev: Dict[int, Optional[int]] = {node: None for node in graph}
    pq = [(heuristic(start), 0.0, start)]

    while pq:
        f, g, u = heapq.heappop(pq)
        if u == end:
            break
        for v, time_w, dist_w in graph[u]:
            w = time_w if weight_idx == 0 else dist_w
            tentative_g = g_cost[u] + w
            if tentative_g < g_cost[v]:
                g_cost[v] = tentative_g
                prev[v] = u
                heapq.heappush(pq, (tentative_g + heuristic(v), tentative_g, v))

    path, node = [], end
    while node is not None:
        path.append(node)
        node = prev[node]
    path.reverse()

    return path, g_cost[end]


def optimize_multi_stop_route(
    stops: List[Dict],
    algorithm: str = "dijkstra",
    optimize_for: str = "time",
) -> Dict:
    """
    Optimize a multi-stop itinerary using the chosen algorithm.
    Greedy nearest-neighbor first, then exact shortest path between consecutive stops.

    stops: [{"id": int, "lat": float, "lon": float, "name": str}, ...]
    Returns ordered stops, total distance, total travel time, and edges.
    """
    if len(stops) < 2:
        return {
            "ordered_stop_ids": [s["id"] for s in stops],
            "total_distance_km": 0.0,
            "total_travel_time_mins": 0.0,
            "edges": [],
        }

    graph = build_graph(stops)

    # Greedy nearest-neighbor to determine visit order
    unvisited = set(s["id"] for s in stops)
    ordered = [stops[0]["id"]]
    unvisited.remove(stops[0]["id"])

    stop_map = {s["id"]: s for s in stops}

    while unvisited:
        current = ordered[-1]
        current_stop = stop_map[current]
        nearest = min(
            unvisited,
            key=lambda nid: haversine_distance(
                current_stop["lat"], current_stop["lon"],
                stop_map[nid]["lat"], stop_map[nid]["lon"],
            ),
        )
        ordered.append(nearest)
        unvisited.remove(nearest)

    # Compute edges between consecutive stops
    edges = []
    total_dist = 0.0
    total_time = 0.0

    for i in range(len(ordered) - 1):
        src, dst = ordered[i], ordered[i + 1]
        if algorithm == "astar":
            path, cost = astar(stops, graph, src, dst, optimize_for)
        else:
            path, cost = dijkstra(graph, src, dst, optimize_for)

        s = stop_map[src]
        d_stop = stop_map[dst]
        dist = haversine_distance(s["lat"], s["lon"], d_stop["lat"], d_stop["lon"])
        time = estimate_travel_time_mins(dist)

        total_dist += dist
        total_time += time
        edges.append({
            "from_id": src,
            "to_id": dst,
            "distance_km": round(dist, 2),
            "travel_time_mins": round(time, 2),
            "path": path,
        })

    return {
        "ordered_stop_ids": ordered,
        "total_distance_km": round(total_dist, 2),
        "total_travel_time_mins": round(total_time, 2),
        "edges": edges,
    }
