from pydantic import BaseModel
from datetime import datetime

class MessageBase(BaseModel):
    conversation_id: int
    sender_id: int
    content: str

class MessageCreate(MessageBase):
    pass

class MessageResponse(MessageBase):
    id: int
    timestamp: datetime
    read: bool

    class Config:
        orm_mode = True
