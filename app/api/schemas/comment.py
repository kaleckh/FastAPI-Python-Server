
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional



class CommentBase(BaseModel):
    content: str
    user_name: str
    post_id: str
    likes: List[str] = []


class CommentCreate(CommentBase):
    post_id: str 
    
    
class CommentUpdate(CommentBase):
    pass


class CommentResponse(CommentBase):
    id: str
    post_id: str
    user_id: str
    date: datetime
    replies: List["CommentResponse"] = []

    class Config:
        orm_mode = True

