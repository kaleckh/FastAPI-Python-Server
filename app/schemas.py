# from pydantic import BaseModel, EmailStr
# from datetime import datetime
# from typing import List, Optional


# # Base schema for common fields


# # Base schema for common fields
# class CommentBase(BaseModel):
#     content: str
#     user_name: str
#     likes: List[str] = []

# # Schema for creating a new comment
# class CommentCreate(CommentBase):
#     post_id: str  # post_id is required when creating a comment

# # Schema for responding with comment data
# class CommentResponse(CommentBase):
#     id: str
#     post_id: str
#     user_id: str
#     date: datetime
#     replies: List["CommentResponse"] = []

#     class Config:
#         orm_mode = True


# class RepostBase(BaseModel):
#     post_id: str
#     user_id: str

# class RepostCreate(RepostBase):
#     pass

# class RepostResponse(RepostBase):
#     date: datetime

#     class Config:
#         orm_mode = True

# class ConversationBase(BaseModel):
#     pass  # No additional fields in the base schema

# # Schema for creating a new conversation
# class ConversationCreate(ConversationBase):
#     pass  # No extra fields are required

# # Schema for responding with conversation data
# class ConversationResponse(ConversationBase):
#     id: str
#     date: datetime
#     users: List[str] = []  # List of user IDs in the conversation

#     class Config:
#         orm_mode = True
        
# class UsersInConversationsBase(BaseModel):
#     conversation_id: str
#     user_id: str

# class UsersInConversationsCreate(UsersInConversationsBase):
#     pass

# class UsersInConversationsResponse(UsersInConversationsBase):
#     class Config:
#         orm_mode = True
        
#         # Base schema for common fields
# class MessageBase(BaseModel):
#     message: str
#     status: Optional[str] = None

# # Schema for creating a new message
# class MessageCreate(MessageBase):
#     conversation_id: str
#     user_id: str

# # Schema for responding with message data
# class MessageResponse(MessageBase):
#     id: str
#     date: datetime
#     conversation_id: str
#     user_id: str

#     class Config:
#         orm_mode = True

