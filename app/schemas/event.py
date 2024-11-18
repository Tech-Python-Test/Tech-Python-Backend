from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Optional

class EventBase(BaseModel):
    title: str
    description: str
    location: str
    datetime: datetime

class EventCreate(EventBase):
    additional_material: Optional[str] = None

class EventResponse(EventBase):
    id: int
    datetime: datetime
    additional_material: Optional[str] = None
    organizer_id: int

    class Config:
        orm_mode = True

class EventUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    datetime: Optional[datetime]
    location: Optional[str]
    additional_material: Optional[str]

    class Config:
        orm_mode = True