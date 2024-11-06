from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.api.crud import conversation as crud
from app.api.schemas.conversation import ConversationCreate, ConversationUpdate


router = APIRouter()    



@router.get("/conversation/{conversation_id}")
def get_conversation(conversation_id: str, db: Session = Depends(get_db)):
    conversation = crud.get_conversation(db, conversation_id)
    return {"conversation": conversation}



@router.get("/conversations")
def get_conversations(db: Session = Depends(get_db)):
    conversations = crud.get_conversations(db)
    return {"conversations": conversations}



@router.post("/create")
def create_conversation(conversation: ConversationCreate, db: Session = Depends(get_db)):
    conversation = crud.create_conversation(db, conversation)
    return {"conversation": conversation}



@router.put("/update/{conversation_id}")
def update_conversation(conversation_id: str, conversation: ConversationUpdate, db: Session = Depends(get_db)):
    conversation_data = conversation.model_dump(exclude_unset=True)
    conversation = crud.update_conversation(db, conversation_id, conversation_data)
    return {"conversation": conversation}



@router.delete("/delete/{conversation_id}")
def delete_conversation(conversation_id: str, db: Session = Depends(get_db)):
    conversation = crud.delete_conversation(db, conversation_id)
    return {"conversation": conversation}



