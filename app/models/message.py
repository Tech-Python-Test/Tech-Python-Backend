from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from app.database.connection import Base
import datetime

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(String, nullable=False)
    translated_content = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    read = Column(Boolean, default=False)

    # Relaciones
    sender = relationship("User", back_populates="messages")
    conversation = relationship("Conversation", back_populates="messages")
