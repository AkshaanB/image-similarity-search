import io
import os
import boto3
from PIL import Image
from typing import Any
from dotenv import load_dotenv
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from project.lib.load_faiss_index.load_faiss_index import load_faiss_index
from project.lib.retrieve_images.retrieve_images import retrieve_images

load_dotenv()

s3_client = boto3.client('s3', 
                         region_name=os.getenv("AWS_REGION"),
                         aws_access_key_id=os.getenv("ACCESS_KEY_ID"), 
                         aws_secret_access_key=os.getenv("SECRET_ACCESS_KEY"))

router = APIRouter()

@router.post('/get_images', tags=['get_images'])
async def get_images(username: str, query: str) -> Any:
    
    index, image_paths = load_faiss_index(username)

    retrieved_images = retrieve_images(index, query, image_paths)

    if retrieved_images:
        return JSONResponse(
            status_code=200,
            content=retrieved_images
        )

    else:
        return JSONResponse(
            status_code=404,
            content={"message": "File/s not found."}
        )

