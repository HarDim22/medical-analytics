from typing import Dict, List, Tuple, Any

REQUIRED_LAB_FIELDS = ["hb", "wbc", "glucose"]

RANGES = {
    "hb": (9.0, 18.0),
    "wbc": (3.0, 12.0),
    "glucose": (60.0, 200.0),
}

def missing_required_fields(payload: Dict[str, Any]) -> List[str]:
    return [f for f in REQUIRED_LAB_FIELDS if f not in payload or payload.get(f) is None]

def out_of_range_fields(payload: Dict[str, Any]) -> List[Tuple[str, float, float, float]]:
    issues = []
    for field, (mn, mx) in RANGES.items():
        if field in payload and payload[field] is not None:
            try:
                v = float(payload[field])
                if v < mn or v > mx:
                    issues.append((field, v, mn, mx))
            except (ValueError, TypeError):
                issues.append((field, float("nan"), mn, mx))
    return issues
