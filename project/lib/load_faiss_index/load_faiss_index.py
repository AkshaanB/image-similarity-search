import faiss


def load_faiss_index(index_path: str):
    index = faiss.read_index(index_path)
    with open(index_path + '.paths', 'r') as f:
        image_paths = [line.strip() for line in f]

    
    return index, image_paths
