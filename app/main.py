# main.py
from fastapi import FastAPI, Depends
from app.database import SessionLocal
from sqlalchemy.orm import Session
from app.models import User
from app.api.routers import user, post, comment, repost, conversation, message
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
from sqlalchemy.exc import OperationalError
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(post.router, prefix="/posts", tags=["posts"])
app.include_router(comment.router, prefix="/comments", tags=["comments"])
app.include_router(repost.router, prefix="/reposts", tags=["reposts"])
app.include_router(conversation.router, prefix="/conversations", tags=["conversations"])
app.include_router(message.router, prefix="/messages", tags=["messages"])

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")


engine = create_engine(DATABASE_URL)    


try:
    with engine.connect() as connection:
        print("Connected to the database successfully!")
except OperationalError as e:
    logger.error("Failed to connect to the database:", e)



@app.get("/")
def root():
    return {"message": "Server is running"}


# SUPABASE_ANON_KEY='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImtscGtjb3hlcXF5bWZwYWFsd2N1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjUzOTc5ODYsImV4cCI6MjA0MDk3Mzk4Nn0.68JPoGuh6nuNydEVrN5CGmF4KwaoPxOLedzizV6A7WU'
# SUPABASE_URL='https://klpkcoxeqqymfpaalwcu.supabase.co'
# DATABASE_URL="postgresql://postgres.klpkcoxeqqymfpaalwcu:TwitterDupe123%21@aws-0-us-west-1.pooler.supabase.com:6543/postgres?pgbouncer=true&connection_limit=1"
# DIRECT_URL="postgresql://postgres.klpkcoxeqqymfpaalwcu:TwitterDupe123%21@aws-0-us-west-1.pooler.supabase.com:5432/postgres?pgbouncer=true&connection_limit=1"