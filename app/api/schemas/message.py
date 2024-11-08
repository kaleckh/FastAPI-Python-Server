from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional


class MessageBase(BaseModel):
    message: str
    status: Optional[str] = None


class MessageCreate(MessageBase):
    conversation_id: str
    user_id: str


class MessageUpdate(MessageBase):
    pass


class MessageResponse(MessageBase):
    id: str
    date: datetime
    conversation_id: str
    user_id: str

    class Config:
        orm_mode = True
