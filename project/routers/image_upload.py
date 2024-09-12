import io
import os
import uuid
import boto3
from PIL import Image
from typing import Any, List
from dotenv import load_dotenv
from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse

from project.lib.generate_embeddings.generate_embeddings import generate_embeddings
from project.lib.create_faiss_index.create_faiss_index import create_faiss_index

load_dotenv()

s3_client = boto3.client('s3', 
                         region_name=os.getenv("AWS_REGION"),
                         aws_access_key_id=os.getenv("ACCESS_KEY_ID"), 
                         aws_secret_access_key=os.getenv("SECRET_ACCESS_KEY"))

bucket_name = os.getenv("BUCKET_NAME")

router = APIRouter()

@router.post('/image_upload', tags=['image_upload'])
async def image_upload(username: str,
                      files: List[UploadFile] = File(...)) -> Any:
    try:
        return_contents = []
        status_codes = []

        for file in files:
            image_id = uuid.uuid4()
            contents = await file.read()

            if contents:
                image = Image.open(io.BytesIO(contents))

                image_bytes = io.BytesIO()
                image.save(image_bytes, format='JPEG')
                image_bytes.seek(0)

                # save image to the s3 bucket
                s3_client.upload_fileobj(image_bytes, bucket_name, f"{username}/images/{image_id}.jpg")

                embeddings, image_paths = generate_embeddings(username)

                index = create_faiss_index(username, embeddings, image_paths)

                return_contents.append({"message": f"File uploaded. Id: f{image_id}"})
                status_codes.append(200)

            else:
                return_contents.append({"message": "File content missing."})
                status_codes.append(400)

        if all(item == 200 for item in status_codes):
            return JSONResponse(
                status_code=200,
                content={"message": f"File/s uploaded successfully."}
            )
        else:
            return JSONResponse(
                status_code=200,
                content={"message": f"File/s uploaded failed."}
            )
        
    except Exception as e:
        return JSONResponse(
                status_code=400,
                content={"message": f"Error: {str(e)}"}
            )
    
    finally:
        await file.close()
