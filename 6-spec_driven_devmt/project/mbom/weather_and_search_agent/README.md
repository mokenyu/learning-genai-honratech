# 🇨🇲 Cameroon Weather-Augmented Intelligence & Search Agent (WAIS-Agent)

**WAIS-Agent** is an autonomous full-stack AI system built with **FastAPI**, **Streamlit**, and **LangGraph / LangChain** powered by **Google Gemini 3.6 Flash** (`gemini-3.6-flash`). 

The agent is specialized in synthesizing hyper-local atmospheric conditions across Cameroon's 10 administrative regions with live web news and transport intelligence, delivering actionable risk assessments and operational advisories for logistics, agriculture, and public safety.

---

## 🏗️ System Architecture

```text
weather_and_search_agent/
├── backend/
│   ├── main.py                 # FastAPI application server & REST endpoints
│   ├── agent.py                # LangChain ReAct agent loop with create_agent (Gemini 3.6 Flash)
│   ├── tools/
│   │   ├── weather_tool.py     # OpenWeatherMap wrapper with Cameroon regional caching
│   │   └── search_tool.py      # SerpAPI / DuckDuckGo live news & search
│   ├── schemas.py              # Pydantic v2 data models
│   └── config.py               # App configuration & Cameroon city metadata
├── frontend/
│   └── app.py                  # Streamlit interactive UI dashboard
├── tests/
│   ├── test_agent.py           # ReAct loop & parser tests
│   ├── test_tools.py           # Weather & search tool unit tests
│   └── test_api.py             # FastAPI endpoint integration tests
├── .env.example
├── README.md
└── requirements.txt
```

---

## 🚀 Quick Start Guide

### 1. Configure Environment Variables
Copy `.env.example` to `.env` in the repository root or project folder:

```bash
cp .env.example .env
```

Ensure `GEMINI_API_KEY` (or `GOOGLE_API_KEY`) is populated:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

*(Optional: Set `OPENWEATHER_API_KEY` and `SERPAPI_API_KEY` for live upstream cloud feeds. If omitted, the system seamlessly uses the built-in Cameroon Regional Climate Model and DuckDuckGo search fallback).*

### 2. Start the Backend API (FastAPI)
Run the FastAPI server on port 8000:

```bash
uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```
Interactive API documentation will be available at: **http://127.0.0.1:8000/docs**

### 3. Start the Frontend Dashboard (Streamlit)
In a separate terminal window, launch the Streamlit UI:

```bash
streamlit run frontend/app.py
```
Open your browser at: **http://localhost:8501**

---

## 🧪 Running Automated Tests

Run the test suite with `pytest`:

```bash
pytest tests/ -v
```

---

## 🇨🇲 Cameroon Regional Coverage
- **Littoral (Douala)**: Douala Autonomous Port (PAD), Wouri basin drainage, N3 highway.
- **Centre (Yaoundé)**: Administrative transit, cocoa drying guidelines, N1 north corridor.
- **South-West (Buea & Limbe)**: Mount Cameroon microclimates, SONARA refinery logistics, coastal tourism.
- **North-West (Bamenda)**: Western Highlands potato and vegetable agro-basin.
- **North & Far-North (Garoua & Maroua)**: Sudano-Sahelian climate, cotton production, Logone-and-Chari river flood alerts.
- **South (Kribi)**: Kribi Deep Sea Port vessel berthing & gas terminal operations.
- **West (Bafoussam)**: High-altitude plateau food crops and poultry transport.
- **Adamawa (Ngaoundéré)**: Camrail railhead cargo terminus and livestock corridor.
- **East (Bertoua)**: Equatorial timber routes and cross-border transport.
