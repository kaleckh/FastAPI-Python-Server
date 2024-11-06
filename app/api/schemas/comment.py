
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional



class CommentBase(BaseModel):
    content: str
    user_name: str
    likes: List[str] = []


class CommentCreate(CommentBase):
    post_id: str 


class CommentResponse(CommentBase):
    id: str
    post_id: str
    user_id: str
    date: datetime
    replies: List["CommentResponse"] = []

    class Config:
        orm_mode = True

