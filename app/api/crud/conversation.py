from fastapi import Depends
from app.database import SessionLocal
from sqlalchemy import and_, func
from sqlalchemy.orm import Session, joinedload
from app.api.schemas.conversation import ConversationCreate, ConversationUpdate
from app.api.schemas.message import MessageCreate, MessageUpdate
from app.models import Conversation, User, Message, UsersInConversations
from fastapi import FastAPI, Depends
import datetime

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
def get_conversations(db: Session, user_id: int):
    return (
        db.query(Conversation)
        .filter(
            Conversation.users.any(User.id == user_id)  
        )
        .options(
            joinedload(Conversation.users),
            joinedload(Conversation.messages).order_by(Message.date.desc())
        )
        .all()
    )



def get_conversation(db: Session, conversation_id: int):
    return db.query(Conversation).filter(Conversation.id == conversation_id).first()



def create_conversation(db: Session, conversation_data: ConversationCreate):
    
    existing_conversation = (
        db.query(Conversation)
        .join(UsersInConversations)
        .filter(
            and_(
                UsersInConversations.c.user_id.in_([conversation_data.my_id, conversation_data.recipient_id]),
                UsersInConversations.c.conversation_id == Conversation.id,
            )
        )
        .group_by(Conversation.id)
        .having(func.count(UsersInConversations.c.user_id) == 2)
        .first()
    )

    if existing_conversation:
        return existing_conversation

    # Create a new conversation
    new_conversation = Conversation(date=datetime.datetime.utcnow())
    db.add(new_conversation)
    db.flush()  # Get the new conversation ID before committing

    # Add users to the conversation
    my_user = db.query(User).filter(User.id == conversation_data.my_id).first()
    recipient_user = db.query(User).filter(User.id == conversation_data.recipient_id).first()

    if not my_user or not recipient_user:
        raise ValueError("One or both users not found")

    new_conversation.users.append(my_user)
    new_conversation.users.append(recipient_user)

    # Add the first message
    new_message = Message(
        conversation_id=new_conversation.id,
        message=conversation_data.message,
        status="Delivered",
        user_id=conversation_data.my_id,
        date=datetime.datetime.utcnow(),
    )
    db.add(new_message)

    db.commit()
    db.refresh(new_conversation)

    return new_conversation


def create_comment(db: Session, message: MessageCreate):
    db_comment = Message(
        content=message.content,
        user_name=message.user_name,
        post_id=message.post_id,
        likes=message.likes
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment
        
      


def update_conversation(db: Session, conversation_id: int, conversation: ConversationUpdate):
    conversation_data = conversation.model_dump(exclude_unset=True)
    db.query(Conversation).filter(Conversation.id == conversation_id).update(conversation_data)
    db.commit()
    updated_conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    return updated_conversation



def delete_conversation(db: Session, conversation_id: int):
    db.query(Conversation).filter(Conversation.id == conversation_id).delete()
    db.commit()
    return {"message": "Conversation deleted"}