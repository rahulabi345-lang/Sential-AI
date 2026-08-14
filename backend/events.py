from fastapi import APIRouter

router = APIRouter(
    prefix="/events",
    tags=["Events"]
)


@router.get("/")
def get_events():
    return {
        "message": "Events endpoint working"
    }


@router.get("/{event_id}")
def get_event(event_id: int):
    return {
        "event_id": event_id,
        "message": "Event retrieved"
    }