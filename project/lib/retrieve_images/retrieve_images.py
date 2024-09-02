import numpy as np


def retrieve_images(model, index, query: str, image_paths: str, top_k: int):
    query_embeddings = model.encode(query)
    query_embeddings = query_embeddings.astype(np.float32).reshape(1,-1)

    distances, indices = index.search(query_embeddings, top_k)

    retrieved_images = [image_paths[int(idx)] for idx in indices[0]]

    return query, retrieved_images
