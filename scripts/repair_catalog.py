"""
Repair malformed SHL catalog JSON.

Current known issue:
- Some string values are accidentally split across multiple lines,
  making the JSON invalid.

This script repairs the file and validates the repaired output.
"""

import json
from pathlib import Path


RAW_FILE = Path("data/raw/shl_product_catalog.json")
OUTPUT_FILE = Path("data/intermediate/shl_product_catalog_repaired.json")


def repair_catalog():
    print("=" * 60)
    print("SHL Catalog Repair")
    print("=" * 60)

    text = RAW_FILE.read_text(encoding="utf-8")

    # Repair known multiline issue
    repaired_text = text.replace(
        '"name": "Microsoft\n365 (New)",',
        '"name": "Microsoft 365 (New)",'
    )

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(repaired_text, encoding="utf-8")

    try:
        data = json.loads(repaired_text)

        print("✅ Repair successful!")
        print(f"Total assessments: {len(data)}")
        print(f"Saved repaired file to:\n{OUTPUT_FILE}")

    except json.JSONDecodeError as e:
        print("❌ Repair failed!")
        print(e)


if __name__ == "__main__":
    repair_catalog()