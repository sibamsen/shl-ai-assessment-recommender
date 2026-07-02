from pathlib import Path
import json
import numpy as np
from sentence_transformers import SentenceTransformer

ROOT = Path(__file__).resolve().parent.parent

catalog_path = ROOT / "data" / "processed" / "shl_product_catalog_clean.json"
save_path = ROOT / "data" / "embeddings"

save_path.mkdir(parents=True, exist_ok=True)

with open(catalog_path, "r", encoding="utf-8") as f:
    catalog = json.load(f)

model = SentenceTransformer("all-MiniLM-L6-v2")

texts = []

for item in catalog:
    txt = f"""
Name: {item['name']}
Description: {item['description']}
Keys: {', '.join(item['keys'])}
Job Levels: {', '.join(item['job_levels'])}
Duration: {item['duration']}
Languages: {', '.join(item['languages'])}
"""
    texts.append(txt)

embeddings = model.encode(
    texts,
    show_progress_bar=True,
    convert_to_numpy=True
)

np.save(save_path / "assessment_embeddings.npy", embeddings)

print("Done")
print(embeddings.shape)