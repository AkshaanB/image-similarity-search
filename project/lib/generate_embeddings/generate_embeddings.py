import io
import os
import boto3
import config
import logging
from PIL import Image
from dotenv import load_dotenv
from typing import Union, List
from sentence_transformers import SentenceTransformer

load_dotenv()

logger = logging.getLogger(__name__)

config.setup_logging()

model = SentenceTransformer('clip-ViT-B-32')

s3_client = boto3.client('s3', 
                         region_name=os.getenv("AWS_REGION"),
                         aws_access_key_id=os.getenv("ACCESS_KEY_ID"), 
                         aws_secret_access_key=os.getenv("SECRET_ACCESS_KEY"))

bucket_name = os.getenv("BUCKET_NAME")
base_url = f"https://{bucket_name}.s3.amazonaws.com/"


def get_image_paths(username: str) -> List[str]:

    logger.info("Retrieving image paths.")

    image_patterns = ['.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.webp']

    response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=f"{username}/images")

    image_files_urls = []
    if 'Contents' in response:
        for item in response['Contents']:
            if any(item['Key'].lower().endswith(ext) for ext in image_patterns):
                url = f"{base_url}{item['Key']}"
                image_files_urls.append(url)
    
    if image_files_urls:
        logger.info("Successfully retrieved the image paths.")

        return image_files_urls
    
    else:
        logger.info("Retrieving image paths failed.")

        return []


def generate_embeddings(username: str) -> Union[List, List]:\

    logger.info("Generating the embeddings.")
    
    image_paths = get_image_paths(username)

    embeddings = []
    for img_path in image_paths:
        img_path = img_path.replace(base_url, "")
        
        # download image from the s3 bucket
        response = s3_client.get_object(Bucket=bucket_name, Key=f"{img_path}")
        content = response["Body"].read()
        image = Image.open(io.BytesIO(content))

        embedding = model.encode(image)
        embeddings.append(embedding)

    if embeddings and image_paths:
        logger.info("Successfully generated the embeddings.")

        return embeddings, image_paths
    else:
        logger.info("Generating the embeddings failed.")

        return None, []


# if __name__=="__main__":

#     embeddings, image_paths = generate_embeddings("")
#     print(embeddings, image_paths)
