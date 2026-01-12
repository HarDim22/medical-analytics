# Medical Web Analytics & Data Quality Monitor (FastAPI)

Event-based analytics microservice for medical workflows (upload → analysis → clinician review).
Tracks funnel performance, data-quality issues, and produces explainable insights.

## Key Features
- Event ingestion (single + bulk) with schema validation (Pydantic)
- Funnel + drop-off analytics
- Data-quality monitoring events (missing fields, out-of-range values)
- Explainable insights (rule-based, evidence-backed)
- API-key protected ingestion + internal metrics
- Public dashboard + public read-only JSON summary
- Persistence via SQLite + SQLAlchemy

## Public Endpoints (no API key)
- Dashboard: `/dashboard`
- Public metrics JSON: `/public/metrics/summary`

## Protected Endpoints (API key required)
Send header: `X-API-Key: <ANALYTICS_API_KEY>`
- Ingest: `POST /events`, `POST /events/bulk`
- Metrics: `GET /metrics/summary`
- Events: `GET /events`

## Run locally (Windows / PowerShell)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

$env:ANALYTICS_API_KEY="change-me-strong"
python create_tables.py
python seed_events.py
python -m uvicorn app.main:app --reload
