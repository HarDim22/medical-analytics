from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Event
from app.analytics import (
    success_rate,
    funnel_counts,
    dropoff,
    top_quality_issues,
    time_to_analysis_minutes,
    explainable_insights,
)

router = APIRouter(tags=["public"])

def _fetch_events(db: Session):
    rows = db.query(Event).order_by(Event.timestamp.asc()).all()

    class E:
        def __init__(self, event_type, entity_id, timestamp):
            self.event_type = event_type
            self.entity_id = entity_id
            self.timestamp = timestamp

    return [E(r.event_type, r.entity_id, r.timestamp) for r in rows]

@router.get("/public/metrics/summary")
def public_metrics_summary(db: Session = Depends(get_db)):
    events = _fetch_events(db)
    return {
        "counts": {"total_events": len(events)},
        "success_rate": success_rate(events),
        "funnel": funnel_counts(events),
        "dropoff": dropoff(events),
        "quality_issues": top_quality_issues(events),
        "time_to_analysis_minutes": time_to_analysis_minutes(events),
        "insights": explainable_insights(events),
        "note": "Public read-only summary (no raw events)."
    }
