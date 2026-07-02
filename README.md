# SHL Assessment Recommender

## Features
- Conversational assessment recommendation
- Semantic search using Sentence Transformers
- FAISS vector retrieval
- Clarification questions before recommendation
- FastAPI REST API
- Swagger UI

## Tech Stack
- Python
- FastAPI
- Sentence Transformers
- FAISS
- Pydantic
- Google Gemini (optional)

## Installation

python -m venv .venv

# Windows
.venv\Scripts\activate

pip install -r requirements.txt

uvicorn app.api.main:app --reload

Open:
http://127.0.0.1:8000/docs