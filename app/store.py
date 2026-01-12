from __future__ import annotations
from typing import List, Optional
from datetime import datetime, timedelta
from app.schemas import AnalyticsEvent

EVENTS: List[AnalyticsEvent] = []

def add_event(e: AnalyticsEvent) -> None:
    EVENTS.append(e)

def list_events(
    since: Optional[datetime] = None,
    until: Optional[datetime] = None,
    entity_id: Optional[str] = None,
    event_type: Optional[str] = None,
) -> List[AnalyticsEvent]:
    out = EVENTS
    if since:
        out = [e for e in out if e.timestamp >= since]
    if until:
        out = [e for e in out if e.timestamp <= until]
    if entity_id:
        out = [e for e in out if e.entity_id == entity_id]
    if event_type:
        out = [e for e in out if e.event_type == event_type]
    return out

def clear_events() -> None:
    EVENTS.clear()

def prune_older_than(days: int) -> int:
    cutoff = datetime.utcnow() - timedelta(days=days)
    before = len(EVENTS)
    keep = [e for e in EVENTS if e.timestamp.replace(tzinfo=None) >= cutoff]
    EVENTS.clear()
    EVENTS.extend(keep)
    return before - len(EVENTS)
