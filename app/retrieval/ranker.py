"""
Ranking module for SHL Assessment Recommender.
"""

from typing import List, Dict


class Ranker:
    """Ranks retrieved assessments."""

    def rank(self, items: List[Dict]) -> List[Dict]:

        ranked = []

        for item in items:

            score = float(item.get("score", 0.0)) * 100

            keys = item.get("keys", [])
            name = item.get("name", "")

            if "Knowledge & Skills" in keys:
                score += 8

            if "Ability & Aptitude" in keys:
                score += 5

            if "Programming" in name:
                score += 5

            item["final_score"] = round(score, 2)

            ranked.append(item)

        ranked.sort(
            key=lambda x: x["final_score"],
            reverse=True,
        )

        return ranked