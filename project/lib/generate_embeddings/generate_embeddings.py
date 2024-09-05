import os
from PIL import Image
from glob import glob
from typing import Union, List
from sentence_transformers import SentenceTransformer


model = SentenceTransformer('clip-ViT-B-32')

def get_image_paths(images_path: str):
    image_patterns = ['.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.webp']

    image_paths = []
    for filename in os.listdir(images_path):
        ext = os.path.splitext(filename)[1].lower()
        
        if ext in image_patterns:
            full_path = os.path.join(images_path, filename)
            image_paths.append(full_path)
    
    return image_paths


def generate_embeddings(images_path: str) -> Union[List, str]:
    image_paths = get_image_paths(images_path)

    embeddings = []
    for img_path in image_paths:
        image = Image.open(img_path)

        embedding = model.encode(image)
        embeddings.append(embedding)

    return embeddings, image_paths
