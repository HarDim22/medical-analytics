from fastapi import APIRouter, Depends
from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Event
from app.security import require_api_key
from app.analytics import (
    success_rate,
    funnel_counts,
    dropoff,
    top_quality_issues,
    time_to_analysis_minutes,
    explainable_insights,
)

router = APIRouter(tags=["metrics"])


def _fetch_events(db: Session, since: Optional[datetime] = None, until: Optional[datetime] = None):
    q = db.query(Event)
    if since:
        q = q.filter(Event.timestamp >= since)
    if until:
        q = q.filter(Event.timestamp <= until)
    rows = q.order_by(Event.timestamp.asc()).all()

    # Convert DB rows to objects that look like AnalyticsEvent (minimal)
    class E:
        def __init__(self, event_type, entity_id, timestamp):
            self.event_type = event_type
            self.entity_id = entity_id
            self.timestamp = timestamp

    return [E(r.event_type, r.entity_id, r.timestamp) for r in rows]


@router.get("/metrics/summary")
def metrics_summary(
    since: Optional[datetime] = None,
    until: Optional[datetime] = None,
    db: Session = Depends(get_db),
    _: bool = Depends(require_api_key),
):
    events = _fetch_events(db, since=since, until=until)

    return {
        "window": {"since": since, "until": until},
        "counts": {"total_events": len(events)},
        "success_rate": success_rate(events),
        "funnel": funnel_counts(events),
        "dropoff": dropoff(events),
        "quality_issues": top_quality_issues(events),
        "time_to_analysis_minutes": time_to_analysis_minutes(events),
        "insights": explainable_insights(events),
    }
