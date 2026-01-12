import os
from datetime import datetime, timezone

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_public_metrics_works():
    r = client.get("/public/metrics/summary")
    assert r.status_code == 200
    assert "counts" in r.json()

def test_protected_metrics_requires_api_key():
    r = client.get("/metrics/summary")
    assert r.status_code in (401, 500)  # 500 only if ANALYTICS_API_KEY not set

def test_ingest_requires_api_key():
    payload = {
        "event_type": "data_upload_started",
        "entity_id": "SUB-T-001",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "actor_role": "patient",
        "metadata": {"source": "test"},
    }
    r = client.post("/events", json=payload)
    assert r.status_code in (401, 500)
