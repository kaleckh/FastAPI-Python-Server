from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.api.crud import repost as crud
from app.api.schemas.repost import RepostCreate


router = APIRouter()    

@router.post("/create")
def create_repost(repost: RepostCreate, db: Session = Depends(get_db)):
    repost = crud.create_repost(db, repost)
    return {"repost": repost}


@router.delete("/delete/{repost_id}")
def delete_repost(repost_id: str, db: Session = Depends(get_db)):
    repost = crud.delete_repost(db, repost_id)
    return {"repost": repost}