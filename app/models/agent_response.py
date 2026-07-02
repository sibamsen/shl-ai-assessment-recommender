"""
Pydantic response model returned by Gemini.
"""

from typing import List

from pydantic import BaseModel, Field


class AgentResponse(BaseModel):
    """Structured LLM response schema."""

    reply: str = Field(
        description="Conversational response text. Explain recommendations if present. Do NOT generate markdown tables here."
    )

    recommendation_names: List[str] = Field(
        description="Exact names of catalog assessments currently recommended for the shortlist. Empty list if clarifying, comparing, or refusing."
    )

    end_of_conversation: bool = Field(
        description="Set to true ONLY when the user confirms the shortlist is final and the conversation is complete."
    )