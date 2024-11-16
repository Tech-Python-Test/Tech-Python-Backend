from sqlalchemy import Column, Integer, String, Boolean, Text
from sqlalchemy.orm import relationship
from app.database.connection import Base
from app.models.user_conversations import user_conversations, user_events

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    auto_translate = Column(Boolean, default=False)
    profile_picture = Column(String, nullable=True)
    interests = Column(Text, nullable=True)
    skills = Column(Text, nullable=True)
    social_links = Column(Text, nullable=True)

    # Relaciones
    messages = relationship("Message", back_populates="sender", cascade="all, delete-orphan")
    conversations = relationship("Conversation", secondary=user_conversations, back_populates="participants")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")
    organized_events = relationship("Event", back_populates="organizer", cascade="all, delete-orphan")
    events = relationship("Event", secondary=user_events, back_populates="users")
    groups = relationship("GroupMember", back_populates="user")
