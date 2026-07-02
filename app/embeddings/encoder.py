from sentence_transformers import SentenceTransformer
import numpy as np

MODEL = SentenceTransformer("all-MiniLM-L6-v2")


def encode(text: str):

    emb = MODEL.encode([text], convert_to_numpy=True).astype("float32")

    return emb