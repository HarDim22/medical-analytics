"""
Event taxonomy (single source of truth).
Keep event names consistent across ingestion, metrics, and docs.
"""

EVENT_TYPES = {
    "data_upload_started",
    "data_upload_completed",
    "missing_required_field",
    "out_of_range_value_detected",
    "analysis_completed",
    "analysis_failed",
    "clinician_review_started",
    "clinician_review_completed",
}

FUNNEL_STEPS = [
    "data_upload_started",
    "data_upload_completed",
    "analysis_completed",
    "clinician_review_completed",
]

QUALITY_EVENTS = {
    "missing_required_field",
    "out_of_range_value_detected",
}

# Optional: helpful descriptions for README / spec endpoint later
EVENT_DESCRIPTIONS = {
    "data_upload_started": "User started submitting medical/lab data.",
    "data_upload_completed": "Submission completed successfully (payload accepted).",
    "missing_required_field": "Submission missing required clinical fields (data quality issue).",
    "out_of_range_value_detected": "Detected a value outside expected clinical range (data quality issue).",
    "analysis_completed": "Analysis pipeline completed successfully.",
    "analysis_failed": "Analysis pipeline failed (e.g., quality gate, validation, system error).",
    "clinician_review_started": "Clinician began reviewing results.",
    "clinician_review_completed": "Clinician completed review and recorded outcome.",
}
