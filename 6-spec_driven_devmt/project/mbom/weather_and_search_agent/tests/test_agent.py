import pytest
from backend.schemas import AgentRequestPayload, AgentResponseContract
from backend.agent import run_wais_agent, _extract_risk_level, _extract_recommendations


def test_agent_request_payload_validation():
    """TC-05: Asserts Pydantic validation on request payload."""
    payload = AgentRequestPayload(
        query="Heavy rainfall in Douala port impact",
        city="Douala",
        country_code="CM",
        response_mode="executive_brief"
    )
    assert payload.city == "Douala"
    assert payload.country_code == "CM"


def test_extract_risk_level_heuristics():
    """TC-06: Asserts risk parser correctly detects risk categories."""
    assert _extract_risk_level("The operational risk is CRITICAL due to flash flood.") == "CRITICAL"
    assert _extract_risk_level("We assign an ELEVATED risk level.") == "ELEVATED"
    assert _extract_risk_level("Conditions indicate LOW risk for travel.") == "LOW"


def test_extract_recommendations_parser():
    """TC-07: Asserts recommendations extractor parses numbered actions."""
    sample_text = """
    ### Recommended Action Plan
    1. Reroute freight trucks around Pouma.
    2. Secure warehouse tarpaulins.
    3. Monitor river water gauges.
    """
    recs = _extract_recommendations(sample_text)
    assert len(recs) >= 3
    assert "Reroute freight trucks around Pouma" in recs[0]


@pytest.mark.integration
def test_run_wais_agent_e2e():
    """TC-08: Full end-to-end integration test with Gemini 3.6 Flash."""
    payload = AgentRequestPayload(
        query="Assess if rainfall in Douala will delay container clearance at the port.",
        city="Douala",
        country_code="CM",
        response_mode="executive_brief"
    )
    response = run_wais_agent(payload)
    assert isinstance(response, AgentResponseContract)
    assert "Douala" in response.target_location
    assert response.weather_data is not None
    assert response.risk_assessment in ["LOW", "MODERATE", "ELEVATED", "CRITICAL"]
    assert len(response.actionable_recommendations) > 0
