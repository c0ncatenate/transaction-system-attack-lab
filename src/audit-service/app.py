from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI(title="audit-service")


class AuditEvent(BaseModel):
    source: str
    event_type: str
    user_id: int | None = None
    account_id: int | None = None
    detail: str | None = None


EVENTS: List[AuditEvent] = []


@app.post("/log")
async def log_event(event: AuditEvent):
    EVENTS.append(event)
    # In a real system this would go to durable storage; here we just print.
    print(f"[audit] {event}")
    return {"status": "logged"}


@app.get("/events")
async def list_events():
    return EVENTS


@app.get("/health")
async def health():
    return {"status": "ok"}
