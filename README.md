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

python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

$env:ANALYTICS_API_KEY="change-me-strong"
python create_tables.py
python seed_events.py
python -m uvicorn app.main:app --reload

Open:

http://127.0.0.1:8000/dashboard

http://127.0.0.1:8000/public/metrics/summary

http://127.0.0.1:8000/docs


---

## 4) “How to ingest” 

### Example: Ingest one event

curl -X POST "http://127.0.0.1:8000/events" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: change-me-strong" \
  -d '{"event_type":"data_upload_started","entity_id":"SUB-999","timestamp":"2026-01-10T10:00:00Z","actor_role