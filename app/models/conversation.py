from sqlalchemy import Column, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database.connection import Base
from app.models.user import User
from app.models.user_conversations import user_conversations

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    user1_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user2_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    accepted = Column(Boolean, default=False)

    # Relación con los participantes de la conversación
    participants = relationship("User", secondary=user_conversations, back_populates="conversations")

    # Relación con los mensajes en la conversación
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")

    # Relaciones con los modelos de User
    user1 = relationship("User", foreign_keys=[user1_id], backref="conversations_as_user1")
    user2 = relationship("User", foreign_keys=[user2_id], backref="conversations_as_user2")