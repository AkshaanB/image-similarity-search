import os
from PIL import Image
from glob import glob
from typing import Union, List
from sentence_transformers import SentenceTransformer


model = SentenceTransformer('clip-ViT-B-32')

def generate_embeddings(images_path: str) -> Union[List, str]:
    image_paths = glob(os.path.join(images_path, '**/*.jpg'), recursive=True)

    embeddings = []
    for img_path in image_paths:
        image = Image.open(img_path)

        embedding = model.encode(image)
        embeddings.append(embedding)

    return embeddings, image_paths
