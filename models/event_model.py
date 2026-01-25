from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class EventType(str, Enum):
    activity = "activity"
    medical = "medical"
    birthday = "birthday"
    reminder = "reminder"
    school = "school"
    other = "other"

class EventCreate(BaseModel):
    created_by: int
    child_id: int | None = None
    title: str
    type: EventType = EventType.other
    start_at: datetime
    end_at: datetime | None = None
    location: str | None = None
    notes: str | None = None

class EventUpdate(EventCreate):
    id: int
