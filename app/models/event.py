from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database.connection import Base
from app.models.relationship import user_events, characteristic_events
import datetime

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    location = Column(String, nullable=False)
    datetime = Column(DateTime, nullable=False)
    image_url = Column(String, nullable=True)
    additional_material = Column(Text, nullable=True)

    # Relación con el usuario que creó el evento
    organizer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    organizer = relationship("User", back_populates="organized_events")

    # Relación con los usuarios asistentes al evento
    users = relationship(
        "User",
        secondary=user_events,
        back_populates="events"
    )
    characteristics = relationship("Characteristic", secondary=characteristic_events, back_populates="events")
