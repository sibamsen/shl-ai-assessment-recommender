from pathlib import Path
import faiss

ROOT = Path(__file__).resolve().parent.parent.parent

INDEX_PATH = ROOT / "data" / "faiss_index" / "assessment.index"


class FaissIndex:

    def __init__(self):
        self.index = faiss.read_index(str(INDEX_PATH))

    def search(self, embedding, top_k=20):
        scores, indices = self.index.search(embedding, top_k)
        return scores[0], indices[0]