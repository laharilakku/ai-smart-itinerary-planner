# 🗺️ Smart Itinerary — AI-Powered Travel Planner

A full-stack travel planning system that optimizes multi-stop routes using **Dijkstra's Algorithm** and **A\* Search**, recommends attractions via **cosine similarity** and **K-Means clustering**, and tracks travel expenses with multi-currency conversion.

---

## ✨ Features

| Module | Description |
|---|---|
| 🔐 Auth | JWT-based authentication with bcrypt password hashing |
| 🗺️ Route Optimization | Dijkstra & A\* shortest path for multi-stop itineraries |
| 🏛️ Attractions | City-based attraction registry with tags and categories |
| 🤖 Recommendations | Content-based filtering (cosine similarity) + K-Means clustering |
| 🌤️ Weather | Real-time weather & 5-day forecast via OpenWeatherMap |
| 💸 Expenses | Multi-currency expense tracking with budget analytics |
| 📊 Analytics | Trip dashboard with spending breakdown by category |

---

## 🏗️ Tech Stack

- **Backend:** FastAPI, Python 3.11
- **Databases:** PostgreSQL (trips/users/expenses), MongoDB (attraction metadata), Firebase (real-time sync)
- **ML / Algorithms:** Dijkstra, A\* Search, Cosine Similarity, K-Means Clustering (scikit-learn)
- **APIs:** Google Maps (distances), OpenWeatherMap (weather), Firebase Storage
- **Auth:** JWT + bcrypt

---

## 🚀 Quick Start

### 1. Clone & Install
```bash
git clone https://github.com/laharilakku/smart-itinerary.git
cd smart-itinerary
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
cp .env.example .env
# Add your DB URL, API keys for Google Maps and OpenWeatherMap
```

### 3. Set Up Database
```bash
createdb itinerary_db
psql -d itinerary_db -f database/migrations/001_initial_schema.sql
psql -d itinerary_db -f database/seeds/seed_attractions.sql
```

### 4. Run Server
```bash
uvicorn app.main:app --reload --port 8000
```

API docs: **http://localhost:8000/docs**

---

## 📁 Project Structure

```
smart-itinerary/
├── app/
│   ├── main.py                        # FastAPI app entry point
│   ├── api/routes/
│   │   ├── auth.py                    # Register / Login
│   │   ├── trips.py                   # CRUD + route optimization
│   │   ├── attractions.py             # Attraction management
│   │   ├── recommendations.py         # AI-based recommendations
│   │   ├── weather.py                 # Weather forecast
│   │   └── expenses.py                # Multi-currency expense tracking
│   ├── core/
│   │   ├── config.py                  # App settings
│   │   ├── database.py                # Async SQLAlchemy
│   │   └── security.py                # JWT + bcrypt
│   ├── models/models.py               # ORM models
│   ├── schemas/schemas.py             # Pydantic schemas
│   └── services/
│       ├── graph_algorithms.py        # Dijkstra + A* Search
│       ├── recommendation_engine.py   # Cosine similarity + K-Means
│       ├── currency_service.py        # Multi-currency conversion
│       └── weather_service.py         # OpenWeatherMap integration
├── database/
│   ├── migrations/                    # SQL schema
│   └── seeds/                         # Sample attraction data (India)
├── tests/
│   ├── unit/                          # Algorithm & ML unit tests
│   └── integration/                   # API tests
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🤖 Algorithms

### Dijkstra's Algorithm
- Finds shortest path between stops (time or distance)
- Greedy nearest-neighbor ordering for multi-stop tours
- Time complexity: O((V + E) log V)

### A\* Search
- Heuristic: haversine distance to goal
- Typically faster than Dijkstra on geographic graphs
- Falls back to Dijkstra cost-equivalence on small graphs

### Cosine Similarity (Recommendations)
- Feature vectors: one-hot category tags + rating + duration + entry fee
- Returns top-N most similar attractions to a given preference profile

### K-Means Clustering
- Groups attractions into 5 clusters (Cultural, Nature, Food, Adventure, Relaxation)
- Persisted as `cluster_id` on each attraction record

---

## 🧪 Running Tests

```bash
pytest tests/ -v --cov=app
```

---

## 📄 License
MIT License

---

*Built by [Lahari Lakku](https://github.com/laharilakku) | B.Tech CSE (AI) | G. Pullaiah College of Engineering and Technology*
