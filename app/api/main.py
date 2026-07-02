"""
Main entry point for the FastAPI service.
"""

from pathlib import Path
from fastapi import FastAPI
from dotenv import load_dotenv

from app.api.routes import router
from app.conversation.manager import ConversationManager

# Load environment variables
load_dotenv()

app = FastAPI(
    title="SHL Assessment Recommender API",
    description="Conversational SHL assessment recommendation system.",
    version="1.0.0"
)

# Startup event to load catalog and initialize manager
@app.on_event("startup")
def startup_event():
    # Resolve catalog path relative to project root
    project_root = Path(__file__).resolve().parent.parent.parent
    catalog_path = project_root / "data/processed/shl_product_catalog_clean.json"
    
    if not catalog_path.exists():
        raise FileNotFoundError(f"Cleaned catalog not found at {catalog_path}. Please run prep script first.")
        
    print(f"Loading catalog from {catalog_path}...")
    app.state.manager = ConversationManager(catalog_path)
    print("Catalog loaded and ConversationManager initialized successfully.")

# Include endpoints router
app.include_router(router)
