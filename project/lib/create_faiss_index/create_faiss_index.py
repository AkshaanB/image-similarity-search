import numpy as np
import faiss


def create_faiss_index(embeddings: list, image_paths: str, output_path: str):

    dimension = len(embeddings[0])
    index = faiss.IndexFlatIP(dimension)
    index = faiss.IndexIDMap(index)

    vectors = np.array(embeddings).astype(np.float32)

    index.add_with_ids(vectors, np.array(range(len(embeddings))))

    faiss.write_index(index, output_path)

    with open(output_path + '.paths', 'w') as f:
        for img_path in image_paths:
            f.write(img_path + '\n')


    return index
