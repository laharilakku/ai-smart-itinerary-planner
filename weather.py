from fastapi import APIRouter
from app.services.weather_service import get_weather, get_forecast

router = APIRouter()


@router.get("/current/{city}")
async def current_weather(city: str):
    return await get_weather(city)


@router.get("/forecast/{city}")
async def weather_forecast(city: str, days: int = 5):
    return await get_forecast(city, days)
