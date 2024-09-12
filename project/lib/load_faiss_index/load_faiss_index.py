import os
import boto3
import faiss
from dotenv import load_dotenv
from typing import Union, Any, List

load_dotenv()

s3_client = boto3.client('s3', 
                         region_name=os.getenv("AWS_REGION"),
                         aws_access_key_id=os.getenv("ACCESS_KEY_ID"), 
                         aws_secret_access_key=os.getenv("SECRET_ACCESS_KEY"))

bucket_name = os.getenv("BUCKET_NAME")

def load_faiss_index(username: str) -> Union[Any, List]:

    with open(f'project/lib/load_faiss_index/{username}_image_indexes.index', 'wb') as file_obj:
        s3_client.download_fileobj(bucket_name, f"{username}/index/{username}_image_indexes.index", file_obj)

    with open(f'project/lib/load_faiss_index/{username}_image_indexes.index.paths', 'wb') as file_obj:
        s3_client.download_fileobj(bucket_name, f"{username}/index/{username}_image_indexes.index.paths", file_obj)

    index_path = f"project/lib/load_faiss_index/{username}_image_indexes.index"

    index = faiss.read_index(index_path)
    with open(index_path + '.paths', 'r') as f:
        image_paths = [line.strip() for line in f]

    if os.path.exists(index_path):
        os.remove(index_path)

    if os.path.exists(index_path + '.paths'):
        os.remove(index_path + '.paths')

    return index, image_paths


# if __name__=="__main__":

#     index, image_paths = load_faiss_index("")
#     print(index, image_paths)
