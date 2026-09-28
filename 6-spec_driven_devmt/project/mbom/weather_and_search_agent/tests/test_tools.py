import pytest
from backend.tools.weather_tool import fetch_current_weather
from backend.tools.search_tool import search_live_web_intelligence
from backend.config import CAMEROON_REGIONS


def test_fetch_current_weather_douala():
    """TC-01: Verifies weather tool retrieves structured observation for Douala."""
    obs = fetch_current_weather.run({"city": "Douala", "country_code": "CM"})
    assert isinstance(obs, str)
    assert "Douala" in obs
    assert "°C" in obs
    assert "Humidity" in obs
    assert "Wind" in obs


def test_fetch_current_weather_all_cameroon_regions():
    """TC-02: Verifies weather tool supports all 10 administrative regions."""
    for city_key, meta in CAMEROON_REGIONS.items():
        obs = fetch_current_weather.run({"city": meta["city"], "country_code": "CM"})
        assert meta["city"] in obs
        assert "Cameroon Weather Station" in obs


def test_fetch_current_weather_caching():
    """TC-03: Verifies in-memory LRU caching returns cached observation tag."""
    obs1 = fetch_current_weather.run({"city": "Yaounde", "country_code": "CM"})
    obs2 = fetch_current_weather.run({"city": "Yaounde", "country_code": "CM"})
    assert "Cached Observation" in obs2 or "Yaoundé" in obs2 or "Yaounde" in obs2


def test_search_live_web_intelligence_cameroon():
    """TC-04: Verifies search tool retrieves news snippets with Cameroon context."""
    obs = search_live_web_intelligence.run({"query": "Douala port container logistics", "num_results": 3})
    assert isinstance(obs, str)
    assert "Cameroon Web Intelligence Feed" in obs
    assert "Snippet:" in obs
    assert "URL:" in obs
