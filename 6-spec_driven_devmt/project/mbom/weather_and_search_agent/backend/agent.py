import re
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from backend.config import (
    GEMINI_API_KEY,
    DEFAULT_MODEL,
    DEFAULT_TEMPERATURE,
    CAMEROON_REGIONS,
    normalize_city_key
)
from backend.schemas import (
    AgentRequestPayload,
    AgentResponseContract,
    WeatherSnapshot,
    SearchCitation
)
from backend.tools.weather_tool import fetch_current_weather, _WEATHER_CACHE
from backend.tools.search_tool import search_live_web_intelligence, _SEARCH_CACHE


def _build_system_instruction() -> str:
    """Constructs strict Cameroon operational system prompt for the ReAct agent."""
    return """You are WAIS-Agent (Cameroon Weather-Augmented Intelligence & Search Agent), an elite environmental and logistics intelligence agent specialized in the Republic of Cameroon.
Your mission is to analyze weather conditions across Cameroon's 10 regions (Littoral, Centre, South-West, North-West, West, North, Far-North, South, Adamawa, East) and assess their downstream impacts on transportation (N3 Douala-Yaoundé corridor, N1 North corridor), ports (Douala Autonomous Port, Kribi Deep Sea Port), agriculture (cocoa, coffee, cotton, vegetables), and public safety.

You have access to two tools:
1. `fetch_current_weather`: Retrieves physical meteorological metrics for Cameroon cities (Douala, Yaoundé, Bamenda, Buea, Limbe, Garoua, Maroua, Bafoussam, Kribi, Ngaoundéré, Bertoua).
2. `search_live_web_intelligence`: Searches real-time news and ground reports regarding road conditions, port operations, and agricultural advisories in Cameroon.

OPERATIONAL PROTOCOL:
1. Grounding Mandate: You must NEVER invent temperature, rainfall, wind speed, or road status data. All figures must originate from tool observations.
2. Dual-Tool Chaining:
   - For queries requiring environmental impact assessment, ALWAYS invoke `fetch_current_weather` first to establish atmospheric ground truth.
   - Then invoke `search_live_web_intelligence` to capture ground reality, transport advisories, or news.
3. Structured Final Synthesis:
   - Provide a final answer formatted with the following exact markdown sections:
     ### Executive Summary
     ### Atmospheric Metrics Snapshot
     ### Real-Time Ground Impacts & News
     ### Risk Assessment
     (Must state one of: LOW, MODERATE, ELEVATED, or CRITICAL, with clear justification)
     ### Recommended Action Plan
     (Numbered list of 3-4 concrete actionable next steps)"""


def get_agent_executor(temperature: Optional[float] = None):
    """Initializes and compiles the LangChain ReAct Agent with Gemini 3.6 Flash using create_agent."""
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY or GOOGLE_API_KEY must be set in environment.")

    llm_kwargs = {
        "model": DEFAULT_MODEL,
        "google_api_key": GEMINI_API_KEY,
        "max_retries": 3
    }
    # Only set temperature if explicitly provided and model does not use fixed sampling
    if temperature is not None and not any(m in DEFAULT_MODEL for m in ["3.6", "2.5", "thinking"]):
        llm_kwargs["temperature"] = temperature

    llm = ChatGoogleGenerativeAI(**llm_kwargs)

    tools = [fetch_current_weather, search_live_web_intelligence]
    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=_build_system_instruction()
    )
    return agent


def _extract_risk_level(text: str) -> str:
    """Parses computed operational risk level from agent response text."""
    upper_text = text.upper()
    if "CRITICAL" in upper_text:
        return "CRITICAL"
    elif "ELEVATED" in upper_text:
        return "ELEVATED"
    elif "MODERATE" in upper_text:
        return "MODERATE"
    elif "LOW" in upper_text:
        return "LOW"
    return "MODERATE"


def _extract_recommendations(text: str) -> List[str]:
    """Extracts bulleted or numbered actionable recommendations from response text."""
    lines = text.split("\n")
    recs = []
    in_recs = False
    for line in lines:
        if "recommended action" in line.lower() or "action plan" in line.lower() or "recommendations" in line.lower():
            in_recs = True
            continue
        if in_recs:
            clean_line = re.sub(r"^[\d\.\-\*\•\s]+", "", line).strip()
            if clean_line and len(clean_line) > 5:
                recs.append(clean_line)
    if not recs:
        recs = [
            "Monitor localized weather telemetry via National Meteorological Directorate (DMN).",
            "Maintain communication with regional transport syndicates along major corridors.",
            "Verify warehouse storage moisture seals for perishable agricultural commodities."
        ]
    return recs[:5]


def run_wais_agent(payload: AgentRequestPayload) -> AgentResponseContract:
    """
    Executes the full ReAct agent workflow for a Cameroon intelligence query,
    extracts tool observations, and serializes into AgentResponseContract.
    """
    city_name = payload.city.strip()
    city_key = normalize_city_key(city_name)
    meta = CAMEROON_REGIONS.get(city_key, CAMEROON_REGIONS["douala"])
    
    temp = payload.temperature_override if payload.temperature_override is not None else DEFAULT_TEMPERATURE
    agent = get_agent_executor(temperature=temp)

    enhanced_query = (
        f"Target Location: {city_name}, Cameroon (Region: {meta['region']}). "
        f"Inquiry: {payload.query}. "
        f"Formatting Profile: {payload.response_mode}."
    )

    # Execute compiled graph
    result = agent.invoke({"messages": [("user", enhanced_query)]})
    messages = result.get("messages", [])

    # Extract final text and execution trace
    final_text = messages[-1].content if messages else "No response generated."
    if isinstance(final_text, list):
        final_text = "".join([part.get("text", "") if isinstance(part, dict) else str(part) for part in final_text])

    trace_steps: List[str] = []
    for msg in messages:
        msg_type = getattr(msg, "type", str(type(msg)))
        content_preview = str(getattr(msg, "content", ""))[:150].replace("\n", " ")
        trace_steps.append(f"[{msg_type.upper()}]: {content_preview}")

    # Inspect cached weather data for location
    weather_snapshot: Optional[WeatherSnapshot] = None
    cache_key = f"{city_key}_{payload.country_code.upper()}"
    if cache_key in _WEATHER_CACHE:
        _, _, raw_weather = _WEATHER_CACHE[cache_key]
        weather_snapshot = WeatherSnapshot(
            city=raw_weather.get("city", city_name),
            region=raw_weather.get("region", meta["region"]),
            temperature_celsius=float(raw_weather.get("temp_c", meta["baseline_temp"])),
            feels_like_celsius=float(raw_weather.get("feels_like_c", meta["baseline_temp"] + 2.0)),
            condition_description=raw_weather.get("condition", meta["baseline_condition"]),
            humidity_pct=int(raw_weather.get("humidity_pct", meta["baseline_humidity"])),
            wind_speed_kmh=float(raw_weather.get("wind_kmh", meta["baseline_wind_kmh"])),
            pressure_hpa=int(raw_weather.get("pressure_hpa", 1012)),
            alert_banner=None if not raw_weather.get("is_sandbox") else "Offline Cameroon Climate Model"
        )
    else:
        weather_snapshot = WeatherSnapshot(
            city=meta["city"],
            region=meta["region"],
            temperature_celsius=meta["baseline_temp"],
            feels_like_celsius=meta["baseline_temp"] + 2.0,
            condition_description=meta["baseline_condition"],
            humidity_pct=meta["baseline_humidity"],
            wind_speed_kmh=meta["baseline_wind_kmh"],
            pressure_hpa=1012,
            alert_banner="Baseline Regional Model"
        )

    # Extract citations from search cache
    citations: List[SearchCitation] = []
    for _, (_, _, items) in _SEARCH_CACHE.items():
        if isinstance(items, list):
            for item in items:
                citations.append(SearchCitation(
                    title=item.get("title", "News Source"),
                    source_domain=item.get("source", "Web"),
                    url=item.get("url", "https://news.google.com"),
                    snippet=item.get("snippet", "")
                ))
    # Deduplicate citations
    unique_citations = []
    seen_titles = set()
    for c in citations:
        if c.title not in seen_titles:
            seen_titles.add(c.title)
            unique_citations.append(c)

    risk_level = _extract_risk_level(final_text)
    recommendations = _extract_recommendations(final_text)

    return AgentResponseContract(
        executive_summary=final_text,
        target_location=f"{meta['city']}, {meta['region']} Region (Cameroon)",
        weather_data=weather_snapshot,
        web_intelligence=unique_citations[:4],
        risk_assessment=risk_level,
        actionable_recommendations=recommendations,
        timestamp_utc=datetime.now(timezone.utc).isoformat(),
        raw_trace=trace_steps
    )
