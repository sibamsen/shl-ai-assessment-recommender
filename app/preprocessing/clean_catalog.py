import json
from pathlib import Path
import re

def clean_catalog(raw_path: Path, processed_path: Path):
    print("Reading raw catalog...")
    text = raw_path.read_text(encoding="utf-8")
    
    # Fix the known multiline string issues
    text = text.replace('"name": "Microsoft \n    365 (New)",', '"name": "Microsoft 365 (New)",')
    text = text.replace('"name": "Microsoft\n365 (New)",', '"name": "Microsoft 365 (New)",')
    
    data = json.loads(text)
    cleaned_data = []
    
    for item in data:
        # Clean name
        name = item.get("name", "")
        # Replace broken unicode character \uFFFD based on context
        if "\uFFFD" in name:
            if "Verify Interactive" in name:
                name = name.replace("\uFFFD", "–") # Replace with en-dash
            elif "360" in name:
                name = name.replace("\uFFFD", "°") # Replace with degree sign
            else:
                name = name.replace("\uFFFD", "-")
        # Normalize double spaces or spaces around hyphens/en-dashes
        name = re.sub(r'\s+', ' ', name).strip()
        
        # Clean description
        desc = item.get("description", "")
        if "\uFFFD" in desc:
            # Usually double \uFFFD is a double quote, single is single quote
            desc = desc.replace("\uFFFD\uFFFD", '"')
            desc = desc.replace("\uFFFD", "'")
        desc = re.sub(r'\s+', ' ', desc).strip()
        
        # Clean link (strip whitespace)
        link = item.get("link", "").strip()
        
        # Clean duration
        duration = item.get("duration", "").strip()
        if duration.lower() == "untimed":
            duration = "Untimed"
        elif not duration:
            duration = "—"
            
        # Clean keys
        keys = item.get("keys", [])
        keys = [k.strip() for k in keys if k.strip()]
        
        # Clean job levels
        job_levels = item.get("job_levels", [])
        job_levels = [jl.strip() for jl in job_levels if jl.strip()]
        
        # Clean languages
        languages = item.get("languages", [])
        languages = [lang.strip() for lang in languages if lang.strip()]
        
        cleaned_item = {
            "entity_id": item.get("entity_id", "").strip(),
            "name": name,
            "link": link,
            "job_levels": job_levels,
            "languages": languages,
            "duration": duration,
            "description": desc,
            "keys": keys,
            "remote": item.get("remote", "yes").strip(),
            "adaptive": item.get("adaptive", "no").strip(),
        }
        cleaned_data.append(cleaned_item)
        
    processed_path.parent.mkdir(parents=True, exist_ok=True)
    with open(processed_path, "w", encoding="utf-8") as f:
        json.dump(cleaned_data, f, indent=2, ensure_ascii=False)
        
    print(f"[OK] Successfully cleaned and saved {len(cleaned_data)} items to {processed_path}")

if __name__ == "__main__":
    project_root = Path("C:/Users/Dell/Desktop/DATA ANALYTICS/Projects/SHL_AI_Recommender")
    raw_file = project_root / "data/raw/shl_product_catalog.json"
    processed_file = project_root / "data/processed/shl_product_catalog_clean.json"
    clean_catalog(raw_file, processed_file)
