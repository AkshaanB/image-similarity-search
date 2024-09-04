import io
import os
import boto3
from PIL import Image
from typing import Any
from dotenv import load_dotenv
from fastapi import APIRouter
from fastapi.responses import JSONResponse

load_dotenv()

s3_client = boto3.client('s3', 
                         region_name=os.getenv("AWS_REGION"),
                         aws_access_key_id=os.getenv("ACCESS_KEY_ID"), 
                         aws_secret_access_key=os.getenv("SECRET_ACCESS_KEY"))

router = APIRouter()

@router.post('/retrieve_images', tags=['retrieve_images'])
async def retrieve_images(username: str, query: str) -> Any:
    # to do

    try:
        return JSONResponse(
            status_code=400,
            content={"message": "File content missing."}
        )

    except Exception as e:
        return JSONResponse(
                status_code=400,
                content={"message": f"Error: {str(e)}"}
            )
