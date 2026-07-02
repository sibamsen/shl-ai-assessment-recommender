from pathlib import Path
import faiss
import numpy as np

ROOT = Path(__file__).resolve().parent.parent

embeddings = np.load(
    ROOT/"data"/"embeddings"/"assessment_embeddings.npy"
).astype("float32")

faiss.normalize_L2(embeddings)

index = faiss.IndexFlatIP(embeddings.shape[1])

index.add(embeddings)

faiss.write_index(
    index,
    str(ROOT/"data"/"faiss_index"/"assessment.index")
)

print(index.ntotal)