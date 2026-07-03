<div align="center">

# 🚀 SHL AI Assessment Recommender

### AI-Powered Conversational Recommendation System for SHL Assessments

Built with **FastAPI · Next.js · FAISS · Sentence Transformers · Gemini · Railway · Vercel**

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)]()
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green.svg)]()
[![Next.js](https://img.shields.io/badge/Next.js-Frontend-black.svg)]()
[![FAISS](https://img.shields.io/badge/FAISS-Vector_Search-orange.svg)]()
[![Sentence Transformers](https://img.shields.io/badge/SentenceTransformers-Embeddings-red.svg)]()
[![Railway](https://img.shields.io/badge/Backend-Railway-purple.svg)]()
[![Vercel](https://img.shields.io/badge/Frontend-Vercel-black.svg)]

</div>

---

# 🌐 Live Demo

### Frontend

https://shl-ai-assessment-recommender.vercel.app

### Backend API

https://shl-ai-assessment-recommender-production-c834.up.railway.app

### API Documentation

https://shl-ai-assessment-recommender-production-c834.up.railway.app/docs

---

# 📖 Overview

The SHL AI Assessment Recommender is an AI-powered web application that recommends the most suitable SHL assessments based on natural language hiring requirements.

Instead of manually browsing hundreds of assessments, recruiters simply describe the hiring need in plain English.

Example:

> "I want to hire graduate software engineers with strong programming and analytical skills."

The application performs semantic retrieval using Sentence Transformers and FAISS before recommending the most relevant SHL assessments through a conversational interface.

---

# ✨ Features

- 🤖 Conversational AI interface
- 🔍 Semantic Search using Sentence Transformers
- ⚡ FAISS Vector Search
- 🧠 Intelligent assessment recommendation
- 📑 Rich assessment cards
- 🌍 Languages, Duration & Competencies
- 📱 Responsive UI
- 🚀 Railway Deployment
- 🌐 Vercel Deployment
- 📚 Interactive Swagger API Documentation

---

# 🏗 Architecture

```
                 User

                   │

                   ▼

        Next.js Frontend (Vercel)

                   │

          Axios REST API

                   │

                   ▼

         FastAPI Backend (Railway)

                   │

          Conversation Manager

                   │

       Recommendation Service

                   │

        Sentence Transformers

                   │

             FAISS Index

                   │

      SHL Assessment Dataset

                   │

      Recommended Assessments
```

---

# 🛠 Tech Stack

## Frontend

- Next.js
- React
- Tailwind CSS
- Axios
- Framer Motion
- Lucide React

## Backend

- FastAPI
- Pydantic
- Sentence Transformers
- FAISS
- NumPy
- Scikit-learn

## Deployment

- Railway
- Vercel

---

# 📂 Project Structure

```
SHL_AI_Recommender/

├── app/
│   ├── api/
│   ├── conversation/
│   ├── retrieval/
│   ├── services/
│   └── models/
│
├── data/
│
├── scripts/
│
├── shl-frontend/
│   ├── app/
│   ├── components/
│   ├── lib/
│   └── public/
│
├── requirements.txt
├── railway.json
└── README.md
```

---

# 💬 Example Query

```
Hiring graduate software engineers with strong C++ knowledge and analytical skills.
```

Example Recommendation

- C++ Programming
- Software Business Analysis
- Problem Solving
- Java Programming
- Coding Assessment

---

# 🚀 Running Locally

## Backend

```bash
git clone https://github.com/sibamsen/shl-ai-assessment-recommender.git

cd SHL_AI_Recommender

python -m venv .venv

pip install -r requirements.txt

uvicorn app.api.main:app --reload
```

Backend:

```
http://localhost:8000
```

Swagger:

```
http://localhost:8000/docs
```

---

## Frontend

```bash
cd shl-frontend

npm install

npm run dev
```

Frontend:

```
http://localhost:3000
```

---

# 📡 API

### POST

```
/chat
```

Request

```json
{
  "messages": [
    {
      "role": "user",
      "content": "Hiring graduate software engineer"
    }
  ]
}
```

Returns

- AI response
- Recommended assessments
- Duration
- Languages
- Competencies

---

# 📸 Screenshots

Add these screenshots after uploading them to GitHub.

- Homepage
- Chat Interface
- Recommendation Cards
- Swagger API
- Railway Deployment
- Vercel Deployment

---

# ⚠ Known Limitation

Some SHL assessment links currently redirect to the generic SHL Products page because SHL has updated or removed certain product pages after the dataset was collected. Recommendation quality and metadata remain unaffected.

---

# 🔮 Future Improvements

- Multi-platform assessment recommendation
- RAG pipeline
- Conversation memory
- User authentication
- Admin dashboard
- Docker support
- Kubernetes deployment
- Analytics dashboard

---

# 👨‍💻 Author

**Sibam Sen**

GitHub

https://github.com/sibamsen

LinkedIn

[(Add your LinkedIn URL)](https://www.linkedin.com/in/sibam-sen/)

---

# ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub.
