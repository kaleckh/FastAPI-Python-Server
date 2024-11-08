from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.api.crud import comment as crud
from app.api.schemas.comment import CommentCreate, CommentUpdate


router = APIRouter()


@router.post("/create")
def create_comment(comment: CommentCreate, db: Session = Depends(get_db)):
    comment = crud.create_comment(db, comment)
    allComments = crud.get_post_comments(db, comment.post_id)
    return {"allComments": allComments}



@router.delete('/delete/{comment_id}')
def delete_comment(comment_id: str, db: Session = Depends(get_db) ):
    return crud.delete_comment(db, comment_id)




