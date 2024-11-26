from fastapi import FastAPI, UploadFile, Form, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, update
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from supabase import create_client, Client
from PIL import Image
from io import BytesIO
import numpy as np
from app.api.schemas.users import UserCreate, UserUpdate, UploadResponse
from app.models import User, Comment
from blurhash import encode
import os

# Initialize FastAPI app
app = FastAPI()

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
    blurhash = encode(pixel_data, x_components=4, y_components=4)
    return blurhash

@app.post("/upload", response_model=UploadResponse)
async def upload_image(
    id: str = Form(...),
    image: UploadFile = Form(...),
    db: Session = Depends(SessionLocal)
):
    try:
        if not id:
            raise HTTPException(status_code=400, detail="User ID is required.")

        # Read image file into memory
        image_data = await image.read()
        image_buffer = BytesIO(image_data)
        image_pil = Image.open(image_buffer)

        # Calculate blurhash
        try:
            blurhash = calculate_blurhash(image_pil)
            db.execute(
                update(User).where(User.id == id).values(blurhash=blurhash)
            )
            db.commit()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error generating blurhash: {e}")

        # Upload image to Supabase
        try:
            storage_response = supabase.storage().from_("profile-images").upload(
                image.filename, image_data, {"content-type": image.content_type, "upsert": True}
            )
            if storage_response.get("error"):
                raise HTTPException(status_code=500, detail=storage_response["error"].get("message"))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error uploading image: {e}")

        return JSONResponse(
            status_code=200,
            content={"message": "Upload successful", "data": storage_response}
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
