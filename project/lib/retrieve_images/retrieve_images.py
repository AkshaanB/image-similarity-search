import config
import logging
import numpy as np
from typing import List
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

config.setup_logging()

model = SentenceTransformer('clip-ViT-B-32')

def retrieve_images(index, query: str, image_paths: str, top_k: int = 3) -> List[str]:
    logger.info("Retrieving the images.")
    
    query_embeddings = model.encode(query)
    query_embeddings = query_embeddings.astype(np.float32).reshape(1,-1)

    distances, indices = index.search(query_embeddings, top_k)

    retrieved_images = [image_paths[int(idx)] for idx in indices[0]]

    if retrieved_images:
        logger.info("Successfully retrieved the images.")

        return retrieved_images
    
    else:
        logger.info("Retrieving images failed.")

        return []


# if __name__=="__main__":

#     query = ""
#     index, image_paths = load_faiss_index("")
#     retrieved_images = retrieve_images(model, index, query, image_paths)
#     print(retrieved_images)
