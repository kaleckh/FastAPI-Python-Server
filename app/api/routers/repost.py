from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.api.crud import repost as crud
from app.api.schemas.repost import RepostCreate, RepostDelete


router = APIRouter()    

@router.post("/add")
def create_repost(repost: RepostCreate, db: Session = Depends(get_db)):
    repost = crud.create_repost(db, repost)
    return {"repost": repost}


@router.post("/delete")
def delete_repost(request: RepostDelete, db: Session = Depends(get_db)):
    repost = crud.delete_repost(db, request)
    return {"repost": repost}