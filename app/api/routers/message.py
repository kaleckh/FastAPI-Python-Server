from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.api.crud import message as crud
from app.api.schemas.message import MessageCreate, MessageUpdate


router = APIRouter()



@router.get('/last-message/{conversation_id}')
def get_last_message(conversation_id: str, db: Session = Depends(get_db)):
    
    lastMessage = (
            db.query(crud.Message)
            .filter(crud.Message.conversation_id == conversation_id)
            .order_by(crud.Message.date.desc())
            .first()
        )
    if lastMessage is None: 
        raise HTTPException(status_code=404, detail="No messages found")
    
    return {"message": lastMessage}



# @router.put("/update/{message_id}")
# def update_message(message_id: str, message: MessageUpdate, db: Session = Depends(get_db)):
#     message_data = message.model_dump(exclude_unset=True)
#     message = crud.update_message(db, message_id, message_data)
#     return {"message": message}


@router.post("/create")
def create_message(message: MessageCreate, db: Session = Depends(get_db)):
    message = crud.create_message(db, message)
    return {"message": message}


