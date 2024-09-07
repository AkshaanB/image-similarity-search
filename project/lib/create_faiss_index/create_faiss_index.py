import os
import boto3
import faiss
import numpy as np
from dotenv import load_dotenv

load_dotenv()

s3_client = boto3.client('s3', 
                         region_name=os.getenv("AWS_REGION"),
                         aws_access_key_id=os.getenv("ACCESS_KEY_ID"), 
                         aws_secret_access_key=os.getenv("SECRET_ACCESS_KEY"))

bucket_name = os.getenv("BUCKET_NAME")
base_url = f"https://{bucket_name}.s3.amazonaws.com/"


def create_output_path(username: str) -> str:

    return f"{base_url}{username}/index/image_indexes.index"

def create_faiss_index(username: str, embeddings: list, image_paths: str):

    output_path = create_output_path(username)

    dimension = len(embeddings[0])
    index = faiss.IndexFlatIP(dimension)
    index = faiss.IndexIDMap(index)

    vectors = np.array(embeddings).astype(np.float32)

    index.add_with_ids(vectors, np.array(range(len(embeddings))))

    faiss.write_index(index, output_path)

    # with open(output_path + '.paths', 'w') as f:
    #     for img_path in image_paths:
    #         f.write(img_path + '\n')


    return index


if __name__=="__main__":

    from generate_embeddings import generate_embeddings

    embeddings, image_paths = generate_embeddings("akshaanb")
    index = create_faiss_index("akshaanb", embeddings, image_paths)
    print(index)
    