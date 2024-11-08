from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.api.crud import post as crud
from app.api.schemas.posts import PostCreate, PostUpdate


router = APIRouter()

@router.get("/posts")
def read_posts(db: Session = Depends(get_db)):
    posts = crud.get_posts(db)
    return {"posts": posts}


@router.get("/post/{post_id}")
def read_post(post_id: str, db: Session = Depends(get_db)):
    post = crud.get_post(db, post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"post": post}


@router.post("/create")
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    post = crud.create_post(db, post)    
    return {"post": post}


@router.put("/update/{post_id}")
def update_post(post_id: str, post: PostUpdate, db: Session = Depends(get_db)):
    updated_post = crud.update_post(db, post_id, post)
    
    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    return {"post": updated_post}



@router.delete("/delete/{post_id}")
def delete_post(post_id: str, db: Session = Depends(get_db)):
    post = crud.delete_post(db, post_id)
    return {"post": post}
