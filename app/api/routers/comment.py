from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.api.crud import comment as crud
from app.api.schemas.comment import CommentCreate, CommentUpdate


router = APIRouter()


@router.post("/addComment")
def create_comment(comment: CommentCreate, db: Session = Depends(get_db)):
    comment = crud.create_comment(db, comment)
    return {"allComments": comment}


@router.post("/likes")
async def add_like(request: Request, db: Session = Depends(get_db)):
    
    data = await request.json()  
    post_id = data.get("postId")
    user_id = data.get("userId")

    if not post_id or not user_id:
        raise HTTPException(status_code=400, detail="Invalid input data")

    post = crud.add_like(db, post_id=post_id, user_id=user_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"post": {"id": post.id, "likes": post.likes}}




@router.delete('/delete/{comment_id}')
def delete_comment(comment_id: str, db: Session = Depends(get_db) ):
    return crud.delete_comment(db, comment_id)




