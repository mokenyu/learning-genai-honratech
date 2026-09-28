import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_api_root():
    """TC-09: Asserts root landing endpoint returns 200 and docs info."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "active"
    assert "Cameroon" in data["target_region"]


def test_api_health():
    """TC-10: Asserts health endpoint returns healthy status and model name."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["model"] == "gemini-3.6-flash"


def test_api_weather_snapshot():
    """TC-11: Asserts fast weather snapshot endpoint returns valid weather metrics."""
    response = client.get("/api/v1/weather/snapshot?city=Douala&country_code=CM")
    assert response.status_code == 200
    data = response.json()
    assert data["city"] == "Douala"
    assert "temperature_celsius" in data
    assert "humidity_pct" in data


@pytest.mark.integration
def test_api_agent_query():
    """TC-12: Asserts POST /api/v1/agent/query executes agent loop and returns 200."""
    payload = {
        "query": "Is weather safe for transport on the N3 highway between Douala and Yaoundé?",
        "city": "Yaoundé",
        "country_code": "CM",
        "response_mode": "executive_brief"
    }
    response = client.post("/api/v1/agent/query", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "executive_summary" in data
    assert "risk_assessment" in data
    assert "actionable_recommendations" in data
