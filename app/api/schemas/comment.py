
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional



class CommentBase(BaseModel):
    content: str
    userName: str
    post_id: str
    user_id: str
    parent_id: str = None



class CommentCreate(CommentBase):
    pass
    
    
class CommentUpdate(CommentBase):
    pass


class CommentDelete(CommentBase):
    comment_id: str


class CommentResponse(CommentBase):
    id: str
    post_id: str
    user_id: str
    date: datetime
    replies: List["CommentResponse"] = []

    class Config:
        from_attributes = True

