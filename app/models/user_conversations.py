from sqlalchemy import Table, Column, Integer, ForeignKey
from app.database.connection import Base

user_conversations = Table(
    "user_conversations",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("conversation_id", Integer, ForeignKey("conversations.id"), primary_key=True)
)

user_events = Table(
    "user_events",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("event_id", Integer, ForeignKey("events.id"), primary_key=True),
)
