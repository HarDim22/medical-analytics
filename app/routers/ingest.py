from fastapi import APIRouter, Depends
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session

from app.schemas import AnalyticsEvent
from app.database import get_db
from app.models import Event
from app.security import require_api_key

router = APIRouter(tags=["ingest"])


@router.post("/events", status_code=201)
def ingest_event(
    event: AnalyticsEvent,
    db: Session = Depends(get_db),
    _: bool = Depends(require_api_key),
):
    db_event = Event(
        event_type=event.event_type,
        entity_id=event.entity_id,
        timestamp=event.timestamp,
        actor_role=event.actor_role,
        event_data=event.metadata,
    )
    db.add(db_event)
    db.commit()
    return {"status": "recorded"}


@router.post("/events/bulk", status_code=201)
def ingest_bulk(
    events: List[AnalyticsEvent],
    db: Session = Depends(get_db),
    _: bool = Depends(require_api_key),
):
    for event in events:
        db_event = Event(
            event_type=event.event_type,
            entity_id=event.entity_id,
            timestamp=event.timestamp,
            actor_role=event.actor_role,
            event_data=event.metadata,
        )
        db.add(db_event)

    db.commit()
    return {"status": "recorded", "count": len(events)}


@router.get("/events")
def get_events(
    since: Optional[datetime] = None,
    until: Optional[datetime] = None,
    entity_id: Optional[str] = None,
    event_type: Optional[str] = None,
    limit: int = 200,
    db: Session = Depends(get_db),
    _: bool = Depends(require_api_key),
):
    q = db.query(Event)

    if since:
        q = q.filter(Event.timestamp >= since)
    if until:
        q = q.filter(Event.timestamp <= until)
    if entity_id:
        q = q.filter(Event.entity_id == entity_id)
    if event_type:
        q = q.filter(Event.event_type == event_type)

    rows = q.order_by(Event.timestamp.desc()).limit(limit).all()

    # Convert DB rows -> schema-like JSON (same shape as before)
    events = []
    for r in rows:
        events.append({
            "event_type": r.event_type,
            "entity_id": r.entity_id,
            "timestamp": r.timestamp,
            "actor_role": r.actor_role,
            "metadata": r.event_data,
        })

    return {"count": len(events), "events": events}
