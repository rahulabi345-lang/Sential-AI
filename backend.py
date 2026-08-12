from fastapi import FastAPI
from pydantic import BaseModel
from typing import Any

app = FastAPI(title="Sentinel AI Backend")


class SecurityEvent(BaseModel):
    event_type: str
    timestamp: str
    process_name: str
    pid: int
    path: str
    username: str
    details: dict[str, Any] = {}


@app.get("/")
def home():
    return {
        "status": "online",
        "message": "Sentinel AI Backend is running"
    }


@app.post("/events")
def receive_event(event: SecurityEvent):
    print("\n[EVENT RECEIVED]")
    print(event.model_dump())

    return {
        "status": "received",
        "event": event.model_dump()
    }