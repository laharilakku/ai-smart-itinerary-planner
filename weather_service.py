"""
Weather service — wraps the OpenWeatherMap API.
Falls back to mock data if the API key is not set.
"""

import httpx
from app.core.config import settings


async def get_weather(city: str) -> dict:
    """Fetch current weather for a city."""
    if not settings.OPENWEATHER_API_KEY or settings.OPENWEATHER_API_KEY == "your-openweather-key":
        return _mock_weather(city)

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": settings.OPENWEATHER_API_KEY,
        "units": "metric",
    }
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(url, params=params, timeout=5.0)
            resp.raise_for_status()
            data = resp.json()
            return {
                "city": data["name"],
                "temperature_c": data["main"]["temp"],
                "feels_like_c": data["main"]["feels_like"],
                "humidity_pct": data["main"]["humidity"],
                "description": data["weather"][0]["description"],
                "wind_speed_mps": data["wind"]["speed"],
                "source": "openweathermap",
            }
        except Exception:
            return _mock_weather(city)


async def get_forecast(city: str, days: int = 5) -> list:
    """Fetch 5-day weather forecast."""
    if not settings.OPENWEATHER_API_KEY or settings.OPENWEATHER_API_KEY == "your-openweather-key":
        return [_mock_weather(city) for _ in range(days)]

    url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {"q": city, "appid": settings.OPENWEATHER_API_KEY, "units": "metric", "cnt": days * 8}
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(url, params=params, timeout=5.0)
            resp.raise_for_status()
            data = resp.json()
            seen = set()
            forecast = []
            for item in data.get("list", []):
                date = item["dt_txt"].split(" ")[0]
                if date not in seen:
                    seen.add(date)
                    forecast.append({
                        "date": date,
                        "temperature_c": item["main"]["temp"],
                        "description": item["weather"][0]["description"],
                        "humidity_pct": item["main"]["humidity"],
                    })
                if len(forecast) >= days:
                    break
            return forecast
        except Exception:
            return [_mock_weather(city) for _ in range(days)]


def _mock_weather(city: str) -> dict:
    return {
        "city": city,
        "temperature_c": 28.0,
        "feels_like_c": 30.0,
        "humidity_pct": 65,
        "description": "partly cloudy",
        "wind_speed_mps": 3.5,
        "source": "mock",
    }
