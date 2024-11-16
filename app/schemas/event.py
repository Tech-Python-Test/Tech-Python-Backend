from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Optional

class EventBase(BaseModel):
    title: str
    description: str
    location: str
    datetime: datetime

class EventCreate(EventBase):
    image_url: Optional[HttpUrl] = None
    additional_material: Optional[str] = None

class EventResponse(EventBase):
    id: int
    image_url: Optional[HttpUrl] = None
    additional_material: Optional[str] = None
    organizer_id: int

    class Config:
        orm_mode = True
