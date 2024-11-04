# main.py
from fastapi import FastAPI, Depends
from app.database import SessionLocal
from sqlalchemy.orm import Session
from app.models import User
from app.routers import user

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.include_router(user.router, prefix="/users", tags=["users"])


@app.get("/")
def root():
    return {"message": "Server is running"}