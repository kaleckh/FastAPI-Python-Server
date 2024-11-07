from fastapi import Depends
from app.database import SessionLocal
from sqlalchemy.orm import Session, joinedload
from app.api.schemas.conversation import ConversationCreate, ConversationUpdate
from app.models import Conversation, User, Message
from fastapi import FastAPI, Depends

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



def create_conversation(db: Session, conversation: ConversationCreate):
    db_conversation = Conversation(
        content=conversation.content,
        user_name=conversation.user_name,
        likes=conversation.likes,
    )
    db.add(db_conversation)
    db.commit()
    db.refresh(db_conversation)
    return db_conversation



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