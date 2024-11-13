from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.api.crud import post as crud
from app.api.schemas.posts import PostCreate, PostUpdate


router = APIRouter()

@router.get("/getPosts")
async def get_fyp_and_reposts(user_id: str = None, db: Session = Depends(get_db)):
    try:
        posts_and_reposts = crud.get_FYP_and_reposts(db, user_id)
        return {"Posts": posts_and_reposts}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.get("/getMyPosts")
async def get_user_posts(user_id: str = None, email: str = None, db: Session = Depends(get_db)):
    try:
        posts_and_reposts = crud.get_user_posts(db, user_id, email)
        return {"Posts": posts_and_reposts}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


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
