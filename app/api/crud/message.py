from fastapi import Depends
from app.database import SessionLocal
from sqlalchemy.orm import Session
from app.api.schemas.message import MessageCreate, MessageUpdate
from app.models import Message
from fastapi import FastAPI, Depends

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
        
def get_last_message(db: Session, conversation_id: str):
    return db.query(Message).filter(Message.conversation_id == conversation_id).order_by(Message.date.desc()).first()




def create_message(db: Session, message: MessageCreate):
    db_message = Message(
        content=message.content,
        user_name=message.user_name,
        likes=message.likes,
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message