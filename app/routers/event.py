from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.schemas.event import EventCreate, EventResponse, EventUpdate
from app.models.event import Event
from app.models.user import User
from app.database.connection import get_db
from datetime import datetime, date, timezone

router = APIRouter(
    prefix="/events",
    tags=["events"]
)

@router.post("/", response_model=EventResponse)
def create_event(event_data: EventCreate, organizer_id: int, db: Session = Depends(get_db)):
    if event_data.datetime < datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="Event date must be in the future")

    organizer = db.query(User).filter(User.id == organizer_id).first()
    if not organizer:
        raise HTTPException(status_code=404, detail="Organizer not found")

    event = Event(
        title=event_data.title,
        description=event_data.description,
        location=event_data.location,
        datetime=event_data.datetime,
        additional_material=event_data.additional_material,
        organizer_id=organizer_id
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event

@router.get("/events/{event_id}", response_model=EventResponse)
def get_event_by_id(event_id: int, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    return event

@router.get("/events/", response_model=List[EventResponse])
def get_events_by_date(
    event_date: date = Query(None, description="Date to filter events by year, month, and day"),
    db: Session = Depends(get_db)
):
    if event_date:
        events = db.query(Event).filter(func.date(Event.datetime) == event_date).all()
    else:
        events = db.query(Event).all()
    
    if not events:
        raise HTTPException(status_code=404, detail="No events found for the specified date")
    
    return events

@router.get("/organizer/{organizer_id}", response_model=List[EventResponse])
def get_events_by_organizer(organizer_id: int, db: Session = Depends(get_db)):
    events = db.query(Event).filter(Event.organizer_id == organizer_id).order_by(Event.datetime).all()
    return events

@router.get("/events/{event_id}/share")
def get_event_share_link(event_id: int, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    event_link = f"http://127.0.0.1:8000/events/{event_id}"
    return {"share_link": event_link}

@router.put("/events/{event_id}/edit", response_model=EventUpdate)
def edit_event(event_id: int, event_data: EventUpdate, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    if event_data.title is not None:
        event.title = event_data.title
    if event_data.description is not None:
        event.description = event_data.description
    if event_data.datetime is not None:
        event.datetime = event_data.datetime
    if event_data.location is not None:
        event.location = event_data.location
    if event_data.additional_material is not None:
        event.additional_material = event_data.additional_material

    db.commit()
    db.refresh(event)

    return event
