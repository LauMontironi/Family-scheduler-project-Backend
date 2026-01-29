from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class EventCreate(BaseModel):
    title: str
    description: Optional[str] = None
    location: Optional[str] = None
    type: str
    start_at: datetime
    end_at: Optional[datetime] = None

class EventUpdate(EventCreate):
    id: int
