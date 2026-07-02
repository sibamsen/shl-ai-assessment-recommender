"""
Assessment data model.

This module defines the internal representation of an SHL assessment.
"""

from typing import List
from pydantic import BaseModel, Field


class Assessment(BaseModel):
    """Represents a single SHL assessment."""

    entity_id: str = Field(..., description="Unique SHL assessment ID")
    name: str
    description: str
    duration: str
    languages: List[str]
    job_levels: List[str]
    keys: List[str]
    remote: str
    adaptive: str
    link: str

    @property
    def test_types(self) -> List[str]:
        """Maps keys to standard Test Type letters."""
        # Special cases from trace analysis
        if "svar" in self.name.lower():
            return ["K"]
        if "development & 360" in [k.lower() for k in self.keys]:
            return ["D"]

        mapping = {
            "Ability & Aptitude": "A",
            "Biodata & Situational Judgment": "B",
            "Competencies": "C",
            "Development & 360": "D",
            "Knowledge & Skills": "K",
            "Personality & Behavior": "P",
            "Simulations": "S",
        }
        types = sorted(list(set(mapping[k] for k in self.keys if k in mapping)))
        return types if types else ["K"]  # Default to K if no key matches

    @property
    def test_type_str(self) -> str:
        """Returns comma-separated Test Type string."""
        return ", ".join(self.test_types)