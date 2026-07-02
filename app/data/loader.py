"""
Loads SHL assessment catalog.
"""

import json
from pathlib import Path
from typing import List

from app.models.assessment import Assessment


def load_catalog(path: Path) -> List[Assessment]:
    """
    Load SHL assessment catalog and convert records
    into Assessment objects.
    """

    if not path.exists():
        raise FileNotFoundError(f"Catalog not found: {path}")

    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)

    return [Assessment(**item) for item in raw]