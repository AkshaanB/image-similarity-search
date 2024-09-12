import numpy as np
from typing import List
from sentence_transformers import SentenceTransformer


model = SentenceTransformer('clip-ViT-B-32')

def retrieve_images(index, query: str, image_paths: str, top_k: int = 3) -> List[str]:
    
    query_embeddings = model.encode(query)
    query_embeddings = query_embeddings.astype(np.float32).reshape(1,-1)

    distances, indices = index.search(query_embeddings, top_k)

    retrieved_images = [image_paths[int(idx)] for idx in indices[0]]

    return retrieved_images


# if __name__=="__main__":

#     query = ""
#     index, image_paths = load_faiss_index("")
#     retrieved_images = retrieve_images(model, index, query, image_paths)
#     print(retrieved_images)
