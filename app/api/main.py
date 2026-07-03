"""
Main entry point for the FastAPI service.
"""

from pathlib import Path

from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.conversation.manager import ConversationManager

# Load environment variables
load_dotenv()

app = FastAPI(
    title="SHL Assessment Recommender API",
    description="Conversational SHL assessment recommendation system.",
    version="1.0.0",
)

# ----------------------------
# CORS Configuration
# ----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://shl-ai-assessment-recommender.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ----------------------------
# Startup
# ----------------------------
@app.on_event("startup")
def startup_event():
    project_root = Path(__file__).resolve().parent.parent.parent

    catalog_path = (
        project_root
        / "data"
        / "processed"
        / "shl_product_catalog_clean.json"
    )

    if not catalog_path.exists():
        raise FileNotFoundError(
            f"Cleaned catalog not found at {catalog_path}"
        )

    print(f"Loading catalog from {catalog_path}...")

    app.state.manager = ConversationManager(catalog_path)

    print("Conversation Manager initialized successfully.")


# ----------------------------
# Routes
# ----------------------------
app.include_router(router)