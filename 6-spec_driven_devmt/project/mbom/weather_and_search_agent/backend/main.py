import time
from fastapi import FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from backend.config import DEFAULT_MODEL, CAMEROON_REGIONS, normalize_city_key
from backend.schemas import (
    AgentRequestPayload,
    AgentResponseContract,
    WeatherSnapshot,
    HealthResponse
)
from backend.agent import run_wais_agent
from backend.tools.weather_tool import fetch_current_weather, _WEATHER_CACHE

app = FastAPI(
    title="Cameroon Weather-Augmented Intelligence & Search Agent (WAIS-Agent)",
    description="Full-stack AI Agent REST API synthesizing Cameroon meteorological conditions with real-time news & search intelligence.",
    version="2.2.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS for Streamlit and cross-origin clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["General"])
def root_redirect():
    """Root landing endpoint providing service metadata and documentation link."""
    return {
        "service": "Cameroon WAIS-Agent API",
        "version": "2.2.0",
        "status": "active",
        "docs": "/docs",
        "target_region": "Republic of Cameroon (10 Administrative Regions)"
    }


@app.get("/api/v1/health", response_model=HealthResponse, tags=["Diagnostics"])
def health_check():
    """Health check endpoint to verify server readiness and active model configuration."""
    return HealthResponse(
        status="healthy",
        service="Cameroon WAIS-Agent Backend",
        region="Cameroon",
        model=DEFAULT_MODEL
    )


@app.get("/api/v1/weather/snapshot", response_model=WeatherSnapshot, tags=["Weather Telemetry"])
def get_weather_snapshot(
    city: str = Query(default="Douala", description="City in Cameroon (e.g. Douala, Yaoundé, Bamenda)"),
    country_code: str = Query(default="CM", description="ISO country code")
):
    """Direct lookup endpoint for fast weather snapshots without full agent reasoning."""
    try:
        # Trigger tool to populate cache / retrieve live metrics
        obs = fetch_current_weather.run({"city": city, "country_code": country_code})
        city_clean = normalize_city_key(city)
        cache_key = f"{city_clean}_{country_code.upper()}"
        
        if cache_key in _WEATHER_CACHE:
            _, _, raw = _WEATHER_CACHE[cache_key]
            return WeatherSnapshot(
                city=raw.get("city", city.title()),
                region=raw.get("region", "Cameroon"),
                temperature_celsius=float(raw.get("temp_c", 28.0)),
                feels_like_celsius=float(raw.get("feels_like_c", 30.0)),
                condition_description=raw.get("condition", "Tropical Weather"),
                humidity_pct=int(raw.get("humidity_pct", 80)),
                wind_speed_kmh=float(raw.get("wind_kmh", 12.0)),
                pressure_hpa=int(raw.get("pressure_hpa", 1012)),
                alert_banner=None if not raw.get("is_sandbox") else "Cameroon Regional Climate Model"
            )
        else:
            meta = CAMEROON_REGIONS.get(city_clean, CAMEROON_REGIONS["douala"])
            return WeatherSnapshot(
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
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve weather snapshot: {str(e)}"
        )


@app.post("/api/v1/agent/query", response_model=AgentResponseContract, tags=["Autonomous Agent"])
def query_agent(payload: AgentRequestPayload):
    """
    Primary endpoint: Dispatches user request to the autonomous ReAct agent,
    executes tool chaining (weather + news), and returns a certified executive deliverable.
    """
    try:
        start_time = time.time()
        response = run_wais_agent(payload)
        return response
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Agent execution encountered an unhandled exception: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)
