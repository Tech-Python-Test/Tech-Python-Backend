from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database.connection import Base
from app.models.relationship import characteristic_events

class Characteristic(Base):
    __tablename__ = "characteristics"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)

    events = relationship("Event", secondary=characteristic_events, back_populates="characteristics")
    

