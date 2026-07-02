"""
Conversation Manager for SHL Assessment Recommender.
"""

from pathlib import Path
from typing import List, Dict, Any

from app.models.assessment import Assessment
from app.data.loader import load_catalog
from app.services.recommendation_service import RecommendationService


class ConversationManager:
    """Conversation manager using semantic retrieval only."""

    def __init__(self, catalog_path: Path):

        self.catalog = load_catalog(catalog_path)

        self.recommender = RecommendationService()

    def format_markdown_table(self, items: List[Assessment]) -> str:

        if not items:
            return ""

        lines = [
            "| # | Name | Test Type | Keys | Duration | Languages | URL |",
            "|---|------|-----------|------|----------|-----------|-----|",
        ]

        for idx, item in enumerate(items, start=1):

            keys = ", ".join(item.keys)

            duration = item.duration or "—"

            if not item.languages:
                languages = "—"

            elif len(item.languages) > 4:

                languages = (
                    ", ".join(item.languages[:4])
                    + f" _(+{len(item.languages)-4} more)_"
                )

            else:

                languages = ", ".join(item.languages)

            lines.append(
                f"| {idx} | {item.name} | "
                f"{item.test_type_str} | "
                f"{keys} | "
                f"{duration} | "
                f"{languages} | "
                f"<{item.link}> |"
            )

        return "\n\n" + "\n".join(lines)

    def process_chat(self, history):

        query = history[-1]["content"].lower()

        purpose_words = [
            "hire", "hiring", "selection",
            "recruit", "development",
            "360", "feedback"
        ]

        role_words = [
            "graduate", "intern",
            "manager", "executive",
            "engineer", "developer",
            "analyst", "sales",
            "leader", "director"
        ]

        has_purpose = any(x in query for x in purpose_words)
        has_role = any(x in query for x in role_words)

        if not has_purpose:
            return {
                "reply": "Before I recommend assessments, are these for hiring (selection), employee development, or 360 feedback?",
                "recommendations": [],
                "end_of_conversation": False,
            }

        if not has_role:
            return {
                "reply": "What is the target role or seniority (e.g. Graduate, Manager, Executive, Software Engineer)?",
                "recommendations": [],
                "end_of_conversation": False,
            }

        retrieved = self.recommender.recommend(query)

        assessments = []
        recommendations = []

        for item in retrieved:

            assessment = Assessment(**item)

            assessments.append(assessment)

            recommendations.append(
                {
                    "name": assessment.name,
                    "url": assessment.link,
                    "test_type": assessment.test_type_str,
                }
            )

        reply = "Based on your requirements, here are the most relevant SHL assessments."

        reply += self.format_markdown_table(assessments)

        return {
            "reply": reply,
            "recommendations": recommendations,
            "end_of_conversation": False,
        }