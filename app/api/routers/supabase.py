from fastapi import FastAPI, UploadFile, Form, HTTPException, Depends, APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, update
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from supabase import create_client, Client
from PIL import Image
from io import BytesIO
import numpy as np
# from app.api.schemas.supabase import UserCreate, UserUpdate, UploadResponse
from app.models import User, Comment
from blurhash import encode
import os

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter()    


# Database setup
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Supabase setup
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

if not SUPABASE_URL or not SUPABASE_ANON_KEY:
    raise ValueError("Missing Supabase URL or Anon Key in environment variables.")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)



# Helper function to calculate blurhash
def calculate_blurhash(image: Image.Image) -> str:
    image = image.resize((64, 64)).convert("RGBA")
    pixel_data = np.array(image, dtype=np.uint8)
    width, height = image.size
    blurhash = encode(pixel_data, components_x=4, components_y=4)  # Correct argument names
    return blurhash


# response_model=UploadResponse
@router.post("/upload")
async def upload_image(
    id: str = Form(...),
    image: UploadFile = Form(...),
    db: Session = Depends(get_db)
):
    try:
        # Read image data
        image_data = await image.read()

        # Generate a unique filename
        unique_filename = f"{id}"

        # Upload image to Supabase
        storage_response = supabase.storage.from_("profile-images").upload(
            unique_filename,
            image_data,
            {"content-type": image.content_type}
        )

        # Handle errors from Supabase
        # if storage_response.get("error"):
        #     raise HTTPException(status_code=500, detail=storage_response["error"]["message"])

        # Construct public URL for the uploaded image
        image_url = f"{SUPABASE_URL}/storage/v1/object/public/profile-images/{unique_filename}"

        return {"message": "Upload successful", "image_url": image_url}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")