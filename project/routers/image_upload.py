import io
import os
import uuid
import boto3
from PIL import Image
from typing import Any
from dotenv import load_dotenv
from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse

load_dotenv()

s3_client = boto3.client('s3', 
                         region_name=os.getenv("AWS_REGION"),
                         aws_access_key_id=os.getenv("ACCESS_KEY_ID"), 
                         aws_secret_access_key=os.getenv("SECRET_ACCESS_KEY"))

router = APIRouter()

@router.post('/image_upload', tags=['image_upload'])
async def image_upload(username: str,
                      file: UploadFile = File(...)) -> Any:
    try:
        image_id = uuid.uuid4()
        contents = await file.read()

        if contents:
            image = Image.open(io.BytesIO(contents))

            image_bytes = io.BytesIO()
            image.save(image_bytes, format='JPEG')
            image_bytes.seek(0)

            # save image to s3 bucket
            s3_client.upload_fileobj(image_bytes, f"{username}", f"images/{image_id}.jpg")

            return JSONResponse(
                status_code=200,
                content={"message": f"File uploaded. Id: f{image_id}"}
            )
        else:
             return JSONResponse(
                status_code=400,
                content={"message": "File content missing."}
            )

    except Exception as e:
        return JSONResponse(
                status_code=400,
                content={"message": f"Error: {str(e)}"}
            )
    
    finally:
        await file.close()
