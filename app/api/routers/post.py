from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.api.crud import post as crud
from app.api.schemas.posts import PostCreate, PostUpdate
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


router = APIRouter()

@router.get("/getPosts")
async def get_fyp_and_reposts(user_id: str = None, db: Session = Depends(get_db)):
    try:
        posts_and_reposts = crud.get_FYP_and_reposts(db, user_id)
        return {"Posts": posts_and_reposts}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    
@router.get("/getPost")
async def get_post(post_id: str = None, db: Session = Depends(get_db)):
    try:
        specific_post = crud.get_post(db, post_id)
        return {"post": specific_post}
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
async def create_post(post: PostCreate, req: Request, db: Session = Depends(get_db)):
    # Log the raw request body
    raw_body = await req.json()
    logger.info("Raw Request Body: %s", raw_body)

    # Log the parsed Pydantic model
    logger.info("Parsed Request Model: %s", post.model_dump())

    # Proceed with creating the post
    created_post = crud.create_post(db, post)
    return {"post": created_post}


@router.post("/likes")
async def add_like(request: Request, db: Session = Depends(get_db)):
    
    
    data = await request.json()  
    
    logger.info("Raw Request Body: %s", data)
    
    post_id = data.get("postId")
    user_id = data.get("userId")

    if not post_id or not user_id:
        raise HTTPException(status_code=400, detail="Invalid input data")

    post = crud.add_like(db, post_id=post_id, user_id=user_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"post": {"id": post.id, "likes": post.likes}}



@router.put("/update/{post_id}")
def update_post(post_id: str, post: PostUpdate, db: Session = Depends(get_db)):
    updated_post = crud.update_post(db, post_id, post)
    
    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    return {"post": updated_post}



@router.delete("/delete")
def delete_post(post_id: str, db: Session = Depends(get_db)):
    post = crud.delete_post(db, post_id)
    return {"post": post}
