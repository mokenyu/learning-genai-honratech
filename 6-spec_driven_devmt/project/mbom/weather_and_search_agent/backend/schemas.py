from datetime import datetime, timezone
from typing import Literal, Optional, List
from pydantic import BaseModel, Field

# -------------------------------------------------------------
# 1. CLIENT REQUEST PAYLOAD
# -------------------------------------------------------------
class AgentRequestPayload(BaseModel):
    """Client request ingested by the FastAPI backend from Streamlit."""
    query: str = Field(
        ...,
        min_length=3,
        max_length=500,
        description="User query regarding weather conditions, logistics, agriculture, or travel in Cameroon."
    )
    city: str = Field(
        default="Douala",
        description="Target city or region in Cameroon (e.g., Douala, Yaounde, Bamenda, Buea, Garoua, Maroua, Kribi)."
    )
    country_code: str = Field(
        default="CM",
        description="ISO 3166-1 alpha-2 country code (defaults to 'CM' for Cameroon)."
    )
    response_mode: Literal["executive_brief", "actionable_bulletins", "raw_data"] = Field(
        default="executive_brief",
        description="Desired formatting profile for the final output."
    )
    temperature_override: Optional[float] = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
        description="Sampling temperature for Gemini 3.6 Flash reasoning."
    )


# -------------------------------------------------------------
# 2. TOOL INPUT SCHEMAS
# -------------------------------------------------------------
class OpenWeatherInput(BaseModel):
    """Schema for OpenWeather Tool invocation."""
    city: str = Field(
        ...,
        min_length=2,
        description="Target city name in Cameroon (e.g. 'Douala', 'Yaounde', 'Bamenda', 'Buea', 'Garoua', 'Maroua', 'Kribi')."
    )
    country_code: Optional[str] = Field(
        default="CM",
        description="Two-letter country code (defaults to 'CM')."
    )
    units: Literal["metric", "imperial"] = Field(
        default="metric",
        description="Measurement units: 'metric' (Celsius, m/s) standard for Cameroon."
    )


class SerpAPIInput(BaseModel):
    """Schema for SerpAPI / Web Search Tool invocation."""
    query: str = Field(
        ...,
        min_length=3,
        max_length=250,
        description="Target search query with Cameroon local context."
    )
    search_type: Literal["search", "news"] = Field(
        default="news",
        description="Search vertical: live 'news' or general 'search'."
    )
    num_results: int = Field(
        default=5,
        ge=1,
        le=10,
        description="Number of organic result snippets to retrieve."
    )


# -------------------------------------------------------------
# 3. RESPONSE DELIVERABLE MODELS
# -------------------------------------------------------------
class WeatherSnapshot(BaseModel):
    """Extracted physical atmospheric metrics."""
    city: str
    region: Optional[str] = None
    temperature_celsius: float
    feels_like_celsius: float
    condition_description: str
    humidity_pct: int
    wind_speed_kmh: float
    pressure_hpa: int
    alert_banner: Optional[str] = None


class SearchCitation(BaseModel):
    """Validated news and web search intelligence citation."""
    title: str
    source_domain: str
    url: str
    snippet: str


class AgentResponseContract(BaseModel):
    """Certified final deliverable payload emitted by FastAPI to Streamlit."""
    executive_summary: str = Field(..., description="High-level synthesis of weather and ground conditions.")
    target_location: str = Field(..., description="City and Region in Cameroon.")
    weather_data: Optional[WeatherSnapshot] = Field(None, description="Atmospheric metrics.")
    web_intelligence: List[SearchCitation] = Field(default_factory=list, description="Validated news & web citations.")
    risk_assessment: Literal["LOW", "MODERATE", "ELEVATED", "CRITICAL"] = Field(
        ...,
        description="Operational risk level for transport, agriculture, or safety."
    )
    actionable_recommendations: List[str] = Field(..., description="Actionable next steps for Cameroon operators.")
    timestamp_utc: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
        description="ISO 8601 UTC timestamp of agent execution."
    )
    raw_trace: Optional[List[str]] = Field(default_factory=list, description="Agent execution trace steps.")


class HealthResponse(BaseModel):
    """Backend service health check response model."""
    status: str
    service: str
    region: str
    model: str
    timestamp_utc: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
