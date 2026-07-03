"""
Conversation Manager for SHL Assessment Recommender.
"""

from pathlib import Path
from typing import List

from app.models.assessment import Assessment
from app.data.loader import load_catalog
from app.services.recommendation_service import RecommendationService


class ConversationManager:
    """Conversation manager using semantic retrieval only."""

    def __init__(self, catalog_path: Path):

        self.catalog = load_catalog(catalog_path)

        self.recommender = RecommendationService()

    def process_chat(self, history):

        query = history[-1]["content"].lower()

        purpose_words = [
            "hire",
            "hiring",
            "selection",
            "recruit",
            "development",
            "360",
            "feedback",
        ]

        role_words = [
            "graduate",
            "intern",
            "manager",
            "executive",
            "engineer",
            "developer",
            "analyst",
            "sales",
            "leader",
            "director",
        ]

        has_purpose = any(x in query for x in purpose_words)
        has_role = any(x in query for x in role_words)

        if not has_purpose:
            return {
                "reply": (
                    "Before I recommend SHL assessments, "
                    "are these for hiring (selection), employee development, "
                    "or 360 feedback?"
                ),
                "recommendations": [],
                "end_of_conversation": False,
            }

        if not has_role:
            return {
                "reply": (
                    "What is the target role or seniority? "
                    "For example: Graduate, Software Engineer, "
                    "Manager or Executive."
                ),
                "recommendations": [],
                "end_of_conversation": False,
            }

        retrieved = self.recommender.recommend(query)

        recommendations = []

        for item in retrieved:

            assessment = Assessment(**item)

            recommendations.append(
                {
                    "name": assessment.name,
                    "url": assessment.link,
                    "test_type": assessment.test_type_str,
                    "duration": assessment.duration,
                    "languages": assessment.languages,
                    "keys": assessment.keys,
                }
            )

        reply = (
            f"I found {len(recommendations)} SHL assessments "
            "that best match your hiring requirements.\n\n"
            "You can review each recommendation below and "
            "open the assessment directly from its card."
        )

        return {
            "reply": reply,
            "recommendations": recommendations,
            "end_of_conversation": False,
        }