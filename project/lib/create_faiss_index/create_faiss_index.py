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


def create_faiss_index(username: str, embeddings: list, image_paths: str):

    output_path = f'./{username}_image_indexes.index'

    dimension = len(embeddings[0])
    index = faiss.IndexFlatIP(dimension)
    index = faiss.IndexIDMap(index)

    vectors = np.array(embeddings).astype(np.float32)

    index.add_with_ids(vectors, np.array(range(len(embeddings))))

    faiss.write_index(index, output_path)

    with open(output_path + '.paths', 'w') as f:
        for img_path in image_paths:
            f.write(img_path + '\n')

    with open(output_path, 'rb') as file_obj:
        # save index file to the s3 bucket
        s3_client.upload_fileobj(file_obj, bucket_name, f"{username}/index/{username}_image_indexes.index")

    with open(output_path + '.paths', 'rb') as file_obj:
        # save path file to the s3 bucket
        s3_client.upload_fileobj(file_obj, bucket_name, f"{username}/index/{username}_image_indexes.index.paths")

    if os.path.exists(output_path):
        os.remove(output_path)

    if os.path.exists(output_path + '.paths'):
        os.remove(output_path + '.paths')

    return index


# if __name__=="__main__":

#     embeddings, image_paths = generate_embeddings("akshaanb")
#     index = create_faiss_index("akshaanb", embeddings, image_paths)
#     print(index)
    