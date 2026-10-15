from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import auth, trips, attractions, recommendations, weather, expenses
from app.core.config import settings
from app.core.database import init_db

app = FastAPI(
    title="Smart Itinerary — AI-Powered Travel Planner",
    description="Multi-stop route planning with Dijkstra & A* search, ML-based attraction recommendations, and expense tracking.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    await init_db()

app.include_router(auth.router,            prefix="/api/auth",            tags=["Authentication"])
app.include_router(trips.router,           prefix="/api/trips",           tags=["Trips"])
app.include_router(attractions.router,     prefix="/api/attractions",     tags=["Attractions"])
app.include_router(recommendations.router, prefix="/api/recommendations", tags=["Recommendations"])
app.include_router(weather.router,         prefix="/api/weather",         tags=["Weather"])
app.include_router(expenses.router,        prefix="/api/expenses",        tags=["Expenses"])

@app.get("/")
async def root():
    return {"message": "Smart Itinerary API is running", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
