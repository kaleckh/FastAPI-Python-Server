from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware  # Import CORS middleware
from app.database import SessionLocal
from sqlalchemy.orm import Session
from app.models import User
from app.api.routers import user, post, comment, repost, conversation, message, supabase
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
from sqlalchemy.exc import OperationalError
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()

# CORS configuration
origins = [
    "http://localhost",
    "http://localhost:3000", 
    "https://social-mobile.vercel.app/",
    "https://fast-api-python-server.vercel.app"     
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],   # Allows all HTTP methods
    allow_headers=["*"],   # Allows all headers
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Include your routers
app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(post.router, prefix="/posts", tags=["posts"])
app.include_router(comment.router, prefix="/comments", tags=["comments"])
app.include_router(repost.router, prefix="/reposts", tags=["reposts"])
app.include_router(conversation.router, prefix="/conversations", tags=["conversations"])
app.include_router(message.router, prefix="/messages", tags=["messages"])
app.include_router(supabase.router, prefix="/supabase", tags=["supabase"])

# Load environment variables
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)    

# Check database connection
try:
    with engine.connect() as connection:
        print("Connected to the database successfully!")
except OperationalError as e:
    logger.error("Failed to connect to the database:", e)

@app.get("/")
def root():
    return {"message": "Server is running"}
