from sentence_transformers import SentenceTransformer
import pickle

model = SentenceTransformer("all-MiniLM-L6-v2")


def dataframe_to_text(df):
    """
    Convert dataframe rows into text format for embedding.
    """
    texts = []
    for _, row in df.iterrows():
        text = f"{row['asset']} in {row['sector']} sector has return {row['return']} risk {row['risk']} volatility {row['volatility']}"
        texts.append(text)
    return texts


def create_embeddings(texts):
    embeddings = model.encode(texts)
    return embeddings


def save_embeddings(embeddings, path):
    with open(path, "wb") as f:
        pickle.dump(embeddings, f)


def load_embeddings(path):
    with open(path, "rb") as f:
        return pickle.load(f)