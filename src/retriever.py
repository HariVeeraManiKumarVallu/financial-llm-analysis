import numpy as np

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def retrieve(query_vector, embeddings, texts, top_k=1):
    """
    Retrieve most relevant financial rows.
    """
    similarities = []

    for emb in embeddings:
        sim = cosine_similarity(query_vector, emb)
        similarities.append(sim)

    indices = np.argsort(similarities)[::-1][:top_k]

    return [texts[i] for i in indices]