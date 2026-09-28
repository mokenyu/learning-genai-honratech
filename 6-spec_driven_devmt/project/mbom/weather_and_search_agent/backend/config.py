import os
import unicodedata
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Google Gemini API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY", "")

# LLM Configuration
DEFAULT_MODEL = "gemini-3.6-flash"
DEFAULT_TEMPERATURE = 0.0
MAX_AGENT_ITERATIONS = 6
MAX_EXECUTION_TIMEOUT = 30.0

# Backend Server Configuration
BACKEND_HOST = os.getenv("BACKEND_HOST", "127.0.0.1")
BACKEND_PORT = int(os.getenv("BACKEND_PORT", "8000"))
BACKEND_URL = os.getenv("BACKEND_URL", f"http://{BACKEND_HOST}:{BACKEND_PORT}")


def normalize_city_key(city: str) -> str:
    """Normalizes accented characters (e.g. Yaoundé -> yaounde, Ngaoundéré -> ngaoundere)."""
    nfkd = unicodedata.normalize("NFKD", city)
    return "".join([c for c in nfkd if not unicodedata.combining(c)]).lower().strip()

# Cameroon 10 Regions & Major Urban Hubs Metadata
CAMEROON_REGIONS: Dict[str, Dict[str, Any]] = {
    "douala": {
        "city": "Douala",
        "region": "Littoral",
        "zone": "Coastal / Equatorial Forest",
        "lat": 4.0511,
        "lon": 9.7679,
        "key_focus": "Douala Autonomous Port (PAD), Wouri basin flooding, N3 freight corridor.",
        "baseline_temp": 28.5,
        "baseline_humidity": 88,
        "baseline_wind_kmh": 14.5,
        "baseline_condition": "Tropical Rain / High Humidity"
    },
    "yaounde": {
        "city": "Yaoundé",
        "region": "Centre",
        "zone": "Guinean Equatorial Plateau",
        "lat": 3.8480,
        "lon": 11.5021,
        "key_focus": "Capital administrative transit, N3 corridor terminal, cocoa agro-logistics.",
        "baseline_temp": 25.0,
        "baseline_humidity": 80,
        "baseline_wind_kmh": 10.0,
        "baseline_condition": "Scattered Clouds / Afternoon Showers"
    },
    "bamenda": {
        "city": "Bamenda",
        "region": "North-West",
        "zone": "Western Highlands",
        "lat": 5.9631,
        "lon": 10.1591,
        "key_focus": "Highland agricultural basin (potatoes, vegetables), feeder road transit.",
        "baseline_temp": 21.0,
        "baseline_humidity": 75,
        "baseline_wind_kmh": 12.0,
        "baseline_condition": "Mild Highlands / Mountain Mist"
    },
    "buea": {
        "city": "Buea",
        "region": "South-West",
        "zone": "Mount Cameroon Volcanic Slope",
        "lat": 4.1539,
        "lon": 9.2435,
        "key_focus": "Mount Cameroon eco-tourism, agro-plantations (bananas, tea), volcanic slopes.",
        "baseline_temp": 22.5,
        "baseline_humidity": 85,
        "baseline_wind_kmh": 15.0,
        "baseline_condition": "Mountain Rain & Cloud Cover"
    },
    "limbe": {
        "city": "Limbe",
        "region": "South-West",
        "zone": "Atlantic Coastal Strip",
        "lat": 4.0167,
        "lon": 9.2167,
        "key_focus": "SONARA refinery logistics, seaside fisheries, Atlantic maritime safety.",
        "baseline_temp": 27.0,
        "baseline_humidity": 86,
        "baseline_wind_kmh": 18.0,
        "baseline_condition": "Coastal Breeze / Warm Showers"
    },
    "bafoussam": {
        "city": "Bafoussam",
        "region": "West",
        "zone": "High-Altitude Agro Plateau",
        "lat": 5.4778,
        "lon": 10.4176,
        "key_focus": "Coffee & poultry supply chains, food crop market prices, highway fog safety.",
        "baseline_temp": 23.0,
        "baseline_humidity": 72,
        "baseline_wind_kmh": 9.5,
        "baseline_condition": "Partly Cloudy / Breezy"
    },
    "garoua": {
        "city": "Garoua",
        "region": "North",
        "zone": "Sudano-Sahelian Savannah",
        "lat": 9.3000,
        "lon": 13.4000,
        "key_focus": "Bénoué river flood monitoring, cotton & grain harvesting, Sahel heat index.",
        "baseline_temp": 34.0,
        "baseline_humidity": 45,
        "baseline_wind_kmh": 16.0,
        "baseline_condition": "Hot & Sunny / High UV"
    },
    "maroua": {
        "city": "Maroua",
        "region": "Far-North",
        "zone": "Sahelian Lake Chad Basin",
        "lat": 10.5972,
        "lon": 14.3158,
        "key_focus": "Logone and Chari seasonal flood risk, drought tracking, Chad cross-border trade.",
        "baseline_temp": 36.5,
        "baseline_humidity": 35,
        "baseline_wind_kmh": 20.0,
        "baseline_condition": "Arid Heat / Dry Wind"
    },
    "kribi": {
        "city": "Kribi",
        "region": "South",
        "zone": "Coastal Deep Sea Port Strip",
        "lat": 2.9378,
        "lon": 9.9078,
        "key_focus": "Kribi Deep Sea Port vessel operations, offshore gas terminals, timber transit.",
        "baseline_temp": 28.0,
        "baseline_humidity": 87,
        "baseline_wind_kmh": 16.5,
        "baseline_condition": "Maritime Coastal Showers"
    },
    "ngaoundere": {
        "city": "Ngaoundéré",
        "region": "Adamawa",
        "zone": "High Plateau Savannah",
        "lat": 7.3167,
        "lon": 13.5833,
        "key_focus": "Cattle & livestock corridor, Camrail railhead cargo terminus, transit hub.",
        "baseline_temp": 26.0,
        "baseline_humidity": 60,
        "baseline_wind_kmh": 13.0,
        "baseline_condition": "Breezy Savannah Skies"
    },
    "bertoua": {
        "city": "Bertoua",
        "region": "East",
        "zone": "Dense Equatorial Rainforest",
        "lat": 4.5772,
        "lon": 13.6844,
        "key_focus": "Timber transport roads, mining logistics, CAR cross-border transit corridor.",
        "baseline_temp": 26.5,
        "baseline_humidity": 82,
        "baseline_wind_kmh": 8.0,
        "baseline_condition": "Equatorial Forest Mist & Rain"
    }
}
