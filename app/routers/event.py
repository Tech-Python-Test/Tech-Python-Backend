from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.event import EventCreate, EventResponse
from app.models.event import Event
from app.models.user import User
from app.database.connection import get_db
from datetime import datetime,timezone

router = APIRouter(
    prefix="/events",
    tags=["events"]
)

@router.post("/", response_model=EventResponse)
def create_event(event_data: EventCreate, organizer_id: int, db: Session = Depends(get_db)):
    # Asegurar que ambas fechas sean offset-aware (con zona horaria UTC)
    if event_data.datetime < datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="Event date must be in the future")

    # Verificar que el organizador exista
    organizer = db.query(User).filter(User.id == organizer_id).first()
    if not organizer:
        raise HTTPException(status_code=404, detail="Organizer not found")

    # Crear el evento
    event = Event(
        title=event_data.title,
        description=event_data.description,
        location=event_data.location,
        datetime=event_data.datetime,
        image_url=str(event_data.image_url) if event_data.image_url else None,
        additional_material=event_data.additional_material,
        organizer_id=organizer_id
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event

@router.get("/", response_model=list[EventResponse])
def get_events(db: Session = Depends(get_db)):
    events = db.query(Event).order_by(Event.datetime).all()
    return events

@router.get("/organizer/{organizer_id}", response_model=list[EventResponse])
def get_events_by_organizer(organizer_id: int, db: Session = Depends(get_db)):
    events = db.query(Event).filter(Event.organizer_id == organizer_id).order_by(Event.datetime).all()
    return events
