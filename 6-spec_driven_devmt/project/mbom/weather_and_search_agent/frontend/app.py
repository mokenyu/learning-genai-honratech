import os
import json
import requests
import streamlit as st
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Cameroon WAIS-Agent | Intelligence Dashboard",
    page_icon="🇨🇲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Backend API Configuration
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

# Cameroon City Presets
CAMEROON_CITIES = [
    "Douala", "Yaoundé", "Bamenda", "Buea", "Limbe",
    "Bafoussam", "Garoua", "Maroua", "Kribi", "Ngaoundéré", "Bertoua"
]

PRESET_QUERIES = {
    "🚢 Douala Port Logistics": {
        "city": "Douala",
        "query": "How is heavy seasonal rainfall in Douala affecting container clearance at the Douala Autonomous Port (PAD) and transport along the N3 corridor?",
        "mode": "executive_brief"
    },
    "🛣️ N3 Highway Freight Safety": {
        "city": "Yaoundé",
        "query": "Check weather and road condition warnings along the N3 Douala-Yaoundé freight highway near Pouma and Édéa.",
        "mode": "actionable_bulletins"
    },
    "🥔 Bamenda Highlands Agro Harvest": {
        "city": "Bamenda",
        "query": "What is the 3-day weather outlook in Bamenda highlands for harvesting and transporting Irish potatoes and market vegetables?",
        "mode": "executive_brief"
    },
    "🌊 Maroua & Far-North Flood Risk": {
        "city": "Maroua",
        "query": "Are there flood advisories or heavy rainfall warnings for the Logone and Chari river basins in Far-North Cameroon today?",
        "mode": "actionable_bulletins"
    },
    "⚓ Kribi Deep Sea Port Operations": {
        "city": "Kribi",
        "query": "Assess maritime wind, swell, and precipitation conditions for container ship berthing at Kribi Deep Sea Port.",
        "mode": "executive_brief"
    }
}


def check_backend_health():
    """Checks if the FastAPI backend server is accessible."""
    try:
        res = requests.get(f"{BACKEND_URL}/api/v1/health", timeout=2.0)
        return res.status_code == 200, res.json() if res.status_code == 200 else {}
    except Exception:
        return False, {}


def fetch_quick_weather(city: str):
    """Fetches fast weather snapshot from backend API or fallback."""
    try:
        res = requests.get(f"{BACKEND_URL}/api/v1/weather/snapshot", params={"city": city, "country_code": "CM"}, timeout=3.0)
        if res.status_code == 200:
            return res.json()
    except Exception:
        pass
    return None


# =============================================================
# SIDEBAR
# =============================================================
with st.sidebar:
    st.markdown("## 🇨🇲 WAIS-Agent Control")
    st.caption("Cameroon Environmental & Logistics Intelligence Engine")
    st.divider()

    # Backend Connection Indicator
    is_healthy, health_data = check_backend_health()
    if is_healthy:
        st.success(f"🟢 Backend Online (`{health_data.get('model', 'gemini-3.6-flash')}`)")
    else:
        st.warning("🟠 Backend Offline — Running in Direct Agent Mode")

    st.subheader("📍 Target Location")
    selected_city = st.selectbox("Select Cameroon Regional Hub:", CAMEROON_CITIES, index=0)
    custom_city = st.text_input("Or Enter Custom City / Town:", placeholder="e.g. Dschang, Ebolowa, Nkongsamba")
    target_city = custom_city.strip() if custom_city.strip() else selected_city

    st.subheader("📋 Response Mode")
    response_mode = st.radio(
        "Select Formatting Profile:",
        ["executive_brief", "actionable_bulletins", "raw_data"],
        format_func=lambda x: {
            "executive_brief": "Executive Brief (Full Report)",
            "actionable_bulletins": "Actionable Bulletins (Field Bullets)",
            "raw_data": "Raw Telemetry & JSON"
        }[x]
    )

    st.subheader("⚙️ Agent Parameters")
    temp_slider = st.slider("Reasoning Temperature:", min_value=0.0, max_value=1.0, value=0.0, step=0.1)

    st.divider()
    st.subheader("💡 Cameroon Presets")
    for preset_name, preset_data in PRESET_QUERIES.items():
        if st.button(preset_name, use_container_width=True):
            st.session_state["query_input"] = preset_data["query"]
            st.session_state["preset_city"] = preset_data["city"]
            st.session_state["preset_mode"] = preset_data["mode"]
            st.rerun()


# =============================================================
# MAIN DASHBOARD
# =============================================================
st.title("🇨🇲 Cameroon Weather-Augmented Intelligence & Search Agent")
st.markdown(
    "**Autonomous Environmental & Logistics Intelligence System** — Synthesizing real-time atmospheric "
    "telemetry across Cameroon's 10 regions with ground intelligence, transport corridors, and news."
)

# Top KPI Weather Metrics Banner
weather_data = fetch_quick_weather(target_city)
if weather_data:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(
            label=f"🌡️ Temp ({weather_data['city']})",
            value=f"{weather_data['temperature_celsius']}°C",
            delta=f"Feels like {weather_data['feels_like_celsius']}°C"
        )
    with col2:
        st.metric(label="💧 Relative Humidity", value=f"{weather_data['humidity_pct']}%")
    with col3:
        st.metric(label="💨 Wind Speed", value=f"{weather_data['wind_speed_kmh']} km/h")
    with col4:
        st.metric(label="⛅ Condition", value=weather_data['condition_description'])
else:
    st.info(f"📍 Target Region: **{target_city}, Cameroon** | Ready to ingest operational query.")

st.divider()

# Query Input Form
default_query = st.session_state.get(
    "query_input",
    f"Analyze weather conditions in {target_city} and assess impacts on road transport and local commerce."
)

with st.form("agent_query_form"):
    user_query = st.text_area(
        "Enter your query or request for Cameroon WAIS-Agent:",
        value=default_query,
        height=100,
        placeholder="e.g. How is rainfall in Douala affecting container movements at the port and along the N3 highway?"
    )
    
    col_btn, col_info = st.columns([1, 4])
    with col_btn:
        submitted = st.form_submit_button("🚀 Run Autonomous Agent", use_container_width=True, type="primary")
    with col_info:
        st.caption("Powered by **Google Gemini 3.6 Flash** + **OpenWeatherMap** + **Live Search Engine**.")

# =============================================================
# EXECUTION & RESULTS RENDERING
# =============================================================
if submitted and user_query.strip():
    payload = {
        "query": user_query.strip(),
        "city": target_city,
        "country_code": "CM",
        "response_mode": response_mode,
        "temperature_override": temp_slider
    }

    with st.spinner(f"🤖 WAIS-Agent is reasoning, checking weather in {target_city}, and scanning Cameroon ground news..."):
        agent_result = None
        error_msg = None

        # Attempt 1: Call FastAPI Backend
        try:
            res = requests.post(f"{BACKEND_URL}/api/v1/agent/query", json=payload, timeout=40.0)
            if res.status_code == 200:
                agent_result = res.json()
            else:
                error_msg = f"Backend error (HTTP {res.status_code}): {res.text}"
        except Exception as e:
            # Attempt 2: Direct Local Execution Fallback
            try:
                from backend.schemas import AgentRequestPayload
                from backend.agent import run_wais_agent
                req = AgentRequestPayload(**payload)
                contract = run_wais_agent(req)
                agent_result = contract.model_dump()
            except Exception as local_err:
                error_msg = f"Failed to execute agent: {str(e)} | Local fallback error: {str(local_err)}"

        if agent_result:
            st.success("✅ Operational Intelligence Brief Generated Successfully!")

            # 1. Operational Risk Level Badge
            risk = agent_result.get("risk_assessment", "MODERATE")
            risk_colors = {
                "LOW": ("🟢 LOW RISK", "Minimal operational disruption to transport and agriculture."),
                "MODERATE": ("🟡 MODERATE RISK", "Minor delays possible; standard weather precautions advised."),
                "ELEVATED": ("🟠 ELEVATED RISK", "Significant weather hazard active; transport/port delays expected."),
                "CRITICAL": ("🔴 CRITICAL RISK", "Severe storm or flood risk; immediate emergency diversion required.")
            }
            badge_title, badge_desc = risk_colors.get(risk, ("🟡 MODERATE RISK", "Standard advisory."))

            st.markdown(f"### Operational Risk Level: **{badge_title}**")
            st.caption(f"{badge_desc} (Target Location: **{agent_result.get('target_location', target_city)}**)")

            st.divider()

            # 2. Executive Summary
            st.markdown("### 📋 Executive Summary & Environmental Synthesis")
            st.markdown(agent_result.get("executive_summary", "No summary available."))

            # 3. Actionable Recommendations
            recs = agent_result.get("actionable_recommendations", [])
            if recs:
                st.markdown("### ✅ Actionable Operational Next Steps")
                for i, r in enumerate(recs, 1):
                    st.markdown(f"**{i}.** {r}")

            # 4. Ground Intelligence & Web Citations
            citations = agent_result.get("web_intelligence", [])
            if citations:
                st.markdown("### 🌐 Real-Time Ground Intelligence & Citations")
                cols = st.columns(min(len(citations), 2))
                for idx, c in enumerate(citations):
                    with cols[idx % len(cols)]:
                        with st.container(border=True):
                            st.markdown(f"**[{c.get('source_domain', 'News Source')}]** [{c.get('title', 'Article')}]({c.get('url', '#')})")
                            st.write(c.get("snippet", ""))

            # 5. Agent Trace Accordion
            trace = agent_result.get("raw_trace", [])
            if trace:
                with st.expander("🔍 View Step-by-Step Agent Execution Trace (ReAct Loop)"):
                    for step in trace:
                        st.code(step, language="text")

            # 6. Deliverable Download
            st.divider()
            markdown_deliverable = f"""# Cameroon WAIS-Agent Operational Intelligence Deliverable
**Target Location:** {agent_result.get('target_location')}  
**Risk Level:** {risk}  
**Timestamp (UTC):** {agent_result.get('timestamp_utc')}  

---

## Executive Summary
{agent_result.get('executive_summary')}

---

## Actionable Recommendations
""" + "\n".join([f"- {r}" for r in recs]) + """

---
*Generated by Cameroon Weather-Augmented Intelligence & Search Agent (WAIS-Agent)*
"""
            st.download_button(
                label="💾 Download Intelligence Report (.md)",
                data=markdown_deliverable,
                file_name=f"wais_brief_{target_city.lower()}_{agent_result.get('risk_assessment', 'brief').lower()}.md",
                mime="text/markdown"
            )

        elif error_msg:
            st.error(f"Error during agent execution: {error_msg}")
