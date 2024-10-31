# main.py
from fastapi import FastAPI, Depends
from database import SessionLocal
from sqlalchemy.orm import Session
from models import User

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/users")
def read_root(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return { "users": users}


@app.post("/kale")
def post_root():
    return {"message": "Testing a post request!"}
