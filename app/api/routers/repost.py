from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.api.crud import repost as crud
from app.api.schemas.repost import RepostCreate


router = APIRouter()    

@router.post("/add")
def create_repost(repost: RepostCreate, db: Session = Depends(get_db)):
    repost = crud.create_repost(db, repost)
    return {"repost": repost}


@router.delete("/delete")
def delete_repost(user_id: str, post_id: str, db: Session = Depends(get_db)):
    repost = crud.delete_repost(db, user_id, post_id)
    return {"repost": repost}