"""
Semantic Retriever for SHL Assessment Recommender.
"""

import json
from pathlib import Path

from app.embeddings.encoder import encode
from app.retrieval.faiss_index import FaissIndex
from app.retrieval.ranker import Ranker
from app.retrieval.metadata_filter import MetadataFilter

ROOT = Path(__file__).resolve().parent.parent.parent

CATALOG_PATH = ROOT / "data" / "processed" / "shl_product_catalog_clean.json"


class Retriever:
    """Retrieves the most relevant assessments using FAISS."""

    def __init__(self):

        with open(CATALOG_PATH, "r", encoding="utf-8") as f:
            self.catalog = json.load(f)

        self.index = FaissIndex()

        self.ranker = Ranker()

        self.filter = MetadataFilter()

    def retrieve(self, query: str, top_k: int = 20):

        # Encode query
        embedding = encode(query)

        # Search FAISS
        scores, indices = self.index.search(embedding, top_k)

        candidates = []

        for score, idx in zip(scores, indices):

            if idx == -1:
                continue

            item = self.catalog[idx].copy()

            item["score"] = float(score)

            candidates.append(item)

        # Rank candidates
        ranked = self.ranker.rank(candidates)

        # Remove duplicates and keep Top-K
        final_results = self.filter.filter(
            ranked,
            top_k=10
        )

        return final_results