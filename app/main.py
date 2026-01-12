from fastapi import FastAPI
from app.routers import ingest, metrics, dashboard, public_metrics

app = FastAPI(
    title="Medical Web Analytics & Data Quality Monitor",
    version="0.2.0",
    description="Analytics-focused prototype for medical platform flows, data quality and explainable insights.",
)

@app.get("/ping")
def ping():
    return {"status": "pong"}

# Routers
app.include_router(ingest.router)
app.include_router(metrics.router)
app.include_router(dashboard.router)
app.include_router(public_metrics.router)
