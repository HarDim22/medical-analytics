from pydantic import BaseModel, Field
from datetime import datetime
from typing import Any, Dict, Optional, Literal

EventType = Literal[
    "data_upload_started",
    "data_upload_completed",
    "missing_required_field",
    "out_of_range_value_detected",
    "analysis_completed",
    "analysis_failed",
    "clinician_review_started",
    "clinician_review_completed",
]

class AnalyticsEvent(BaseModel):
    event_type: EventType
    entity_id: str = Field(..., description="Anonymized submission/patient identifier (no PII).")
    timestamp: datetime
    actor_role: Optional[Literal["patient", "clinician", "researcher", "system"]] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
