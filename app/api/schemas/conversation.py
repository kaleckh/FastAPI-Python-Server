from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional

class ConversationBase(BaseModel):
    pass  # No additional fields in the base schema

# Schema for creating a new conversation
class ConversationCreate(ConversationBase):
    pass  # No extra fields are required

class ConversationUpdate(ConversationBase):
    pass

class ConversationDelete(ConversationBase):
    conversation_id: str

# Schema for responding with conversation data
class ConversationResponse(ConversationBase):
    id: str
    date: datetime
    users: List[str] = []  # List of user IDs in the conversation

    class Config:
        orm_mode = True
        
class UsersInConversationsBase(BaseModel):
    conversation_id: str
    user_id: str

class UsersInConversationsCreate(UsersInConversationsBase):
    pass

class UsersInConversationsResponse(UsersInConversationsBase):
    class Config:
        orm_mode = True
        
        # Base schema for common fields