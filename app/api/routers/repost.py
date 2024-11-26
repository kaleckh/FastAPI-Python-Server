from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.api.crud import repost as crud
from app.api.schemas.repost import RepostCreate, RepostDelete
import logging

# Configure logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  


router = APIRouter()    

@router.post("/add")
def create_repost(repost: RepostCreate, db: Session = Depends(get_db)):
    logger.debug("stuff: %s", repost)   
    repost = crud.create_repost(db, repost)
    return {"repost": repost}


@router.post("/delete")
def delete_repost(request: RepostDelete, db: Session = Depends(get_db)):
    logger.debug("stuff: %s", request)   
    repost = crud.delete_repost(db, request)
    return {"repost": repost}