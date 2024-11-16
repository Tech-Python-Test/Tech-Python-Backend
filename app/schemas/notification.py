from pydantic import BaseModel
from datetime import datetime

class NotificationResponse(BaseModel):
    id: int
    user_id: int
    message_id: int
    created_at: datetime
    read: bool

    class Config:
        orm_mode = True
