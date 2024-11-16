from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database.connection import Base

class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)

    # Relaciones
    members = relationship("GroupMember", back_populates="group")
    messages = relationship("GroupMessage", back_populates="group")
