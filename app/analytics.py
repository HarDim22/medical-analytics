from __future__ import annotations
from typing import Dict, List, Any
from collections import Counter
from app.schemas import AnalyticsEvent

FUNNEL = [
    "data_upload_started",
    "data_upload_completed",
    "analysis_completed",
    "clinician_review_completed",
]

QUALITY_EVENTS = {"missing_required_field", "out_of_range_value_detected"}

def explainable_insights(events):
    ins = []

    if not events:
        return [{
            "type": "info",
            "message": "No data yet. Ingest events to see metrics and insights.",
            "evidence": {"total_events": 0},
        }]

def _count(events: List[AnalyticsEvent], t: str) -> int:
    return sum(1 for e in events if e.event_type == t)

def success_rate(events: List[AnalyticsEvent]) -> float:
    started = _count(events, "data_upload_started")
    completed = _count(events, "data_upload_completed")
    return (completed / started) if started else 0.0

def funnel_counts(events: List[AnalyticsEvent]) -> Dict[str, int]:
    return {step: _count(events, step) for step in FUNNEL}

def dropoff(events: List[AnalyticsEvent]) -> Dict[str, Any]:
    counts = funnel_counts(events)
    drops = []
    prev = None
    for step in FUNNEL:
        if prev is None:
            prev = step
            continue
        prev_c = counts[prev]
        step_c = counts[step]
        drop = (prev_c - step_c)
        drop_rate = (drop / prev_c) if prev_c else 0.0
        drops.append({"from": prev, "to": step, "drop": drop, "drop_rate": drop_rate})
        prev = step
    return {"counts": counts, "drops": drops}

def top_quality_issues(events: List[AnalyticsEvent]) -> Dict[str, int]:
    c = Counter(e.event_type for e in events if e.event_type in QUALITY_EVENTS)
    return dict(c.most_common())

def time_to_analysis_minutes(events: List[AnalyticsEvent]) -> Dict[str, Any]:
    completed_at = {}
    deltas = []
    for e in sorted(events, key=lambda x: x.timestamp):
        if e.event_type == "data_upload_completed":
            completed_at[e.entity_id] = e.timestamp
        elif e.event_type == "analysis_completed" and e.entity_id in completed_at:
            dt = (e.timestamp - completed_at[e.entity_id]).total_seconds() / 60.0
            if dt >= 0:
                deltas.append(dt)

    if not deltas:
        return {"count": 0, "avg": None, "min": None, "max": None}

    return {
        "count": len(deltas),
        "avg": sum(deltas) / len(deltas),
        "min": min(deltas),
        "max": max(deltas),
    }

def explainable_insights(events: List[AnalyticsEvent]) -> List[Dict[str, Any]]:
    ins: List[Dict[str, Any]] = []
    sr = success_rate(events)
    q = top_quality_issues(events)
    dr = dropoff(events)
    tta = time_to_analysis_minutes(events)

    if sr < 0.8:
        ins.append({
            "type": "workflow",
            "message": f"Only {sr:.0%} of uploads complete successfully; investigate UX and validation bottlenecks.",
            "evidence": {"success_rate": sr},
        })
    else:
        ins.append({
            "type": "workflow",
            "message": f"Upload completion rate is {sr:.0%}, indicating stable intake performance.",
            "evidence": {"success_rate": sr},
        })

    if q:
        main = max(q, key=q.get)
        ins.append({
            "type": "data_quality",
            "message": f"Top data-quality blocker is '{main}' ({q[main]} events). Prioritize data collection and validation improvements.",
            "evidence": {"top_quality_issues": q},
        })
    else:
        ins.append({
            "type": "data_quality",
            "message": "No major data-quality blockers detected in the observed window.",
            "evidence": {"top_quality_issues": q},
        })

    worst = None
    for d in dr["drops"]:
        if worst is None or d["drop_rate"] > worst["drop_rate"]:
            worst = d
    if worst:
        ins.append({
            "type": "funnel",
            "message": f"Largest drop-off occurs from {worst['from']} → {worst['to']} ({worst['drop_rate']:.0%}).",
            "evidence": worst,
        })

    if tta["count"] and tta["avg"] is not None:
        ins.append({
            "type": "performance",
            "message": f"Average time from upload completion to analysis completion is {tta['avg']:.1f} minutes.",
            "evidence": tta,
        })

    return ins
