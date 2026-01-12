from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
from datetime import datetime
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Event
from app.analytics import (
    success_rate,
    funnel_counts,
    top_quality_issues,
    explainable_insights,
)

router = APIRouter(tags=["dashboard"])


def _fetch_events_for_dashboard(db: Session):
    rows = db.query(Event).order_by(Event.timestamp.asc()).all()

    # minimal event-like objects expected by analytics funcs
    class E:
        def __init__(self, event_type, entity_id, timestamp):
            self.event_type = event_type
            self.entity_id = entity_id
            self.timestamp = timestamp

    return [E(r.event_type, r.entity_id, r.timestamp) for r in rows]


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(db: Session = Depends(get_db)):
    events = _fetch_events_for_dashboard(db)

    sr = success_rate(events)
    funnel = funnel_counts(events)
    quality = top_quality_issues(events)
    insights = explainable_insights(events)

    def li(items):
        return "".join(f"<li>{x}</li>" for x in items)

    insight_lines = [i["message"] for i in insights]

    html = f"""
    <html>
      <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>Medical Analytics Monitor</title>
        <style>
          body {{ font-family: Arial, sans-serif; padding: 24px; max-width: 1000px; margin: 0 auto; }}
          .card {{ border: 1px solid #ddd; border-radius: 12px; padding: 16px; margin-bottom: 16px; }}
          .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }}
          .muted {{ color: #666; }}
          code {{ background: #f6f6f6; padding: 2px 6px; border-radius: 6px; }}
        </style>
      </head>
      <body>
        <h1>Medical Web Analytics & Data Quality Monitor</h1>
        <p class="muted">
          Public, read-only dashboard. Metrics are computed from the database.
        </p>
        <p>Total events in DB: <b>{len(events)}</b></p>

        <div class="grid">
          <div class="card">
            <h2>Upload Success Rate</h2>
            <p><b>{sr:.0%}</b></p>
            <p class="muted">
              Based on <code>data_upload_started</code> → <code>data_upload_completed</code>
            </p>
          </div>

          <div class="card">
            <h2>Top Data Quality Issues</h2>
            <ul>{li([f"{k}: {v}" for k, v in quality.items()] or ["No issues detected"])}</ul>
          </div>
        </div>

        <div class="card">
          <h2>Funnel</h2>
          <ul>{li([f"{k}: {v}" for k, v in funnel.items()])}</ul>
        </div>

        <div class="card">
          <h2>Explainable Insights</h2>
          <ul>{li(insight_lines or ["No insights yet. Ingest events first."])}</ul>
        </div>

        <div class="card">
          <h2>How to use</h2>
          <p>Ingest events via <code>POST /events</code> (API key required).</p>
          <p>This dashboard is public and shows aggregated analytics only.</p>
        </div>
      </body>
    </html>
    """
    return html

