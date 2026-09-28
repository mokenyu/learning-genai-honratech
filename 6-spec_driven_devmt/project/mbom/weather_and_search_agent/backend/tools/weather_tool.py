import time
import unicodedata
import requests
from typing import Dict, Any, Optional
from langchain_core.tools import tool, ToolException
from backend.config import OPENWEATHER_API_KEY, CAMEROON_REGIONS
from backend.schemas import OpenWeatherInput

# In-memory LRU Cache: (city.lower(), country_code) -> (timestamp, data_str)
_WEATHER_CACHE: Dict[str, tuple[float, str, Dict[str, Any]]] = {}
CACHE_TTL_SECONDS = 600.0  # 10 minutes


def _normalize_city_key(city: str) -> str:
    """Normalizes accented characters (e.g. Yaoundé -> yaounde, Ngaoundéré -> ngaoundere)."""
    nfkd = unicodedata.normalize("NFKD", city)
    return "".join([c for c in nfkd if not unicodedata.combining(c)]).lower().strip()


def _get_cameroon_sandbox_data(city: str) -> Dict[str, Any]:
    """Generates localized Cameroon meteorological data when offline or in sandbox mode."""
    city_key = _normalize_city_key(city)
    meta = CAMEROON_REGIONS.get(city_key, CAMEROON_REGIONS["douala"])
    
    return {
        "city": meta["city"],
        "region": meta["region"],
        "zone": meta["zone"],
        "temp_c": meta["baseline_temp"],
        "feels_like_c": meta["baseline_temp"] + 2.0,
        "condition": meta["baseline_condition"],
        "humidity_pct": meta["baseline_humidity"],
        "wind_kmh": meta["baseline_wind_kmh"],
        "pressure_hpa": 1012,
        "key_focus": meta["key_focus"],
        "is_sandbox": True
    }


def _format_weather_observation(data: Dict[str, Any]) -> str:
    """Formats raw weather dictionary into structured string for LLM ReAct observation."""
    sandbox_tag = " [OFFLINE CAMEROON CLIMATE SANDBOX]" if data.get("is_sandbox") else " [LIVE OPENWEATHER DATA]"
    return (
        f"[Cameroon Weather Station: {data['city']}, {data.get('region', 'Cameroon')}{sandbox_tag}]\n"
        f"• Agro-Ecological Zone: {data.get('zone', 'Central African Plateau')}\n"
        f"• Temperature: {data['temp_c']}°C (Feels like: {data['feels_like_c']}°C)\n"
        f"• Weather Condition: {data['condition']}\n"
        f"• Relative Humidity: {data['humidity_pct']}%\n"
        f"• Wind Velocity: {data['wind_kmh']} km/h\n"
        f"• Atmospheric Pressure: {data['pressure_hpa']} hPa\n"
        f"• Regional Operational Context: {data.get('key_focus', 'Regional logistics & agriculture')}"
    )


@tool(args_schema=OpenWeatherInput)
def fetch_current_weather(city: str, country_code: Optional[str] = "CM", units: str = "metric") -> str:
    """
    Retrieves current physical meteorological metrics (temperature, humidity, wind, conditions)
    for cities in Cameroon (Douala, Yaoundé, Bamenda, Buea, Limbe, Garoua, Maroua, Kribi, etc.).
    """
    city_clean = city.strip()
    cache_key = f"{city_clean.lower()}_{country_code.upper() if country_code else 'CM'}"
    now = time.time()

    # Check in-memory cache
    if cache_key in _WEATHER_CACHE:
        cached_time, cached_obs, _ = _WEATHER_CACHE[cache_key]
        if now - cached_time < CACHE_TTL_SECONDS:
            return cached_obs + " (Cached Observation)"

    # Live OpenWeather API call
    if OPENWEATHER_API_KEY and len(OPENWEATHER_API_KEY) > 10:
        try:
            url = "https://api.openweathermap.org/data/2.5/weather"
            params = {
                "q": f"{city_clean},{country_code}" if country_code else city_clean,
                "appid": OPENWEATHER_API_KEY,
                "units": units
            }
            response = requests.get(url, params=params, timeout=5.0)
            if response.status_code == 200:
                json_data = response.json()
                parsed = {
                    "city": json_data.get("name", city_clean),
                    "region": CAMEROON_REGIONS.get(city_clean.lower(), {}).get("region", "Cameroon"),
                    "zone": CAMEROON_REGIONS.get(city_clean.lower(), {}).get("zone", "Sub-Saharan"),
                    "temp_c": json_data["main"]["temp"],
                    "feels_like_c": json_data["main"]["feels_like"],
                    "condition": json_data["weather"][0]["description"].title() if json_data.get("weather") else "Clear",
                    "humidity_pct": json_data["main"]["humidity"],
                    "wind_kmh": round(json_data["wind"]["speed"] * 3.6, 1),
                    "pressure_hpa": json_data["main"]["pressure"],
                    "key_focus": CAMEROON_REGIONS.get(city_clean.lower(), {}).get("key_focus", "Urban & Logistics"),
                    "is_sandbox": False
                }
                obs = _format_weather_observation(parsed)
                _WEATHER_CACHE[cache_key] = (now, obs, parsed)
                return obs
            elif response.status_code == 404:
                raise ToolException(f"CityNotFoundError: '{city_clean}' not found in OpenWeather database.")
        except requests.RequestException:
            pass  # Fall through to Cameroon sandbox fallback

    # Fallback: Cameroon Specialized Regional Climate Model
    sandbox_data = _get_cameroon_sandbox_data(city_clean)
    obs = _format_weather_observation(sandbox_data)
    _WEATHER_CACHE[cache_key] = (now, obs, sandbox_data)
    return obs


# Configure tool resilience
fetch_current_weather.handle_tool_error = True
