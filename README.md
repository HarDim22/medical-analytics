# Medical Web Analytics & Data Quality Monitor

Event-based analytics backend for medical data workflows  
(upload → analysis → clinician review).

The system ingests structured events, computes funnel metrics,
tracks data-quality issues, and produces explainable insights.
Designed as a lightweight analytics microservice for healthcare platforms.

---
## 📸 Screenshots

### Analytics Dashboard
![Dashboard](assets/dashboard.png)

### Public Metrics (JSON)
![Public Metrics](assets/public-metrics.png)


## ✨ Key Features

- Event ingestion with schema validation (FastAPI + Pydantic)
- Funnel analytics & drop-off detection
- Data-quality monitoring (missing fields, out-of-range values)
- Explainable insights based on computed metrics
- API-key protected ingestion & internal metrics
- Public read-only dashboard and JSON metrics
- SQLite persistence (demo-friendly)
- Docker-first setup (1-command run)

---

## 🧠 Example Workflow

1. Patient uploads medical data  
2. System validates & analyzes data  
3. Clinician reviews results  
4. Events are logged and analyzed:
   - Success rate
   - Drop-off points
   - Quality bottlenecks
   - Time-to-analysis

---

## 🌐 Public Endpoints (No API Key Required)

- **Dashboard:**  
  `/dashboard`

- **Public Metrics (JSON):**  
  `/public/metrics/summary`

These endpoints expose **aggregated analytics only** (no raw data).

---

## 🔐 Protected Endpoints (API Key Required)

Send header:
X-API-Key: <ANALYTICS_API_KEY>


- `POST /events` – ingest a single event  
- `POST /events/bulk` – ingest multiple events  
- `GET /metrics/summary` – internal analytics  
- `GET /events` – raw events (internal use)

---

## 🚀 Run with Docker (Recommended – 1 Command)

### Requirements
- Docker installed

### Run
docker build -t medical-analytics .
docker run --rm -p 8000:8000 -e ANALYTICS_API_KEY=change-me-strong medical-analytics

Open

http://127.0.0.1:8000/dashboard

http://127.0.0.1:8000/public/metrics/summary

http://127.0.0.1:8000/docs

🖥️ Run Locally (Python)
Requirements

Python 3.11+

Setup
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

Run
python create_tables.py
python seed_events.py
python -m uvicorn app.main:app --reload

📦 Project Structure
medical-analytics/
│
├── app/
│   ├── main.py                 # FastAPI entrypoint
│   │
│   ├── database.py             # DB engine & session
│   ├── models.py               # ORM models
│   ├── schemas.py              # Pydantic schemas
│   ├── security.py             # API key auth
│   ├── store.py                # Persistence helpers
│   ├── events.py               # Event ingestion logic
│   ├── analytics.py            # Metrics & funnel calculations
│   ├── quality_rules.py        # Data quality rules
│   │
│   ├── utils/
│   │   └── timestamps.py       # Time helpers
│   │
│   └── routers/
│       ├── __init__.py
│       ├── ingest.py           # /events endpoints
│       ├── metrics.py          # protected metrics
│       ├── public_metrics.py   # public read-only metrics
│       └── dashboard.py        # dashboard routes
│
├── assets/
│   ├── dashboard.png
│   └── public-metrics.png
│
├── data/
│   └── mock_events.json        # demo / seed data
│
├── tests/
│   └── tests_api.py            # basic API tests
│
├── create_tables.py            # DB initialization
│
├── Dockerfile
├── .dockerignore
│
├── requirements.txt            # runtime deps
├── requirements-dev.txt        # dev / tests deps
│
├── run-local.ps1               # local run
├── run-docker.ps1              # docker demo run
│
├── .gitignore
└── README.md


🔎 Example Event Payload
{
  "event_type": "data_upload_started",
  "entity_id": "SUB-001",
  "timestamp": "2026-01-10T10:00:00Z",
  "actor_role": "patient",
  "metadata": {
    "source": "web"
  }
}

🎯 Use Cases

Medical data pipeline analytics

Data quality monitoring

Clinical workflow optimization

Healthcare platform observability

Web analytics with privacy-safe aggregation

🛠️ Tech Stack

Backend: FastAPI, Python 3.11

ORM: SQLAlchemy

Database: SQLite (demo)

API Docs: OpenAPI / Swagger

Deployment: Docker

Architecture: Event-driven analytics

👤 Author

Dimitra Charizani
BSc Applied Informatics – University of Macedonia

Interests:
AI-driven analytics · Medical data systems · Automation · Explainable insights

📌 Notes

This project is intended as a portfolio and demo system.

No real patient data is used.

Designed to be easily portable to PostgreSQL or cloud environments.