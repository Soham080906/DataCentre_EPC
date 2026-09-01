# Data Centre EPC AI Intelligence Platform

> **Autonomous AI Intelligence Layer for Mission-Critical Data Centre Engineering, Procurement, and Construction (EPC) Project Delivery.**

---

## System Overview

The **Data Centre EPC AI Intelligence Platform** unifies fragmented project documentation across complex data centre builds to eliminate schedule delays, prevent technical non-conformances, and provide real-time project risk intelligence:

1. **Project Knowledge Assistant (RAG)**: Multi-document semantic search with source citations (document name, page number, section, chunk) and strict anti-hallucination guarantees.
2. **Specification Compliance Agent**: Automated parameter extraction from engineering specifications and vendor submittals, evaluated using deterministic Python verification.
3. **Schedule Risk Engine**: Critical path dependency modeling connecting procurement lead times, factory testing, site delivery, and commissioning milestones with downstream impact propagation.
4. **Project Intelligence Dashboard**: Central real-time mission control for project health, compliance matrices, AI alerts, and schedule risk scores.

---

## Quickstart & Local Setup

### Option 1: Using Docker Compose
```bash
cp .env.example .env
docker-compose up --build
```

### Option 2: Running Locally

#### 1. Backend (FastAPI):
```bash
cd backend
python -m venv venv
# Windows:
venv\Scripts\activate
# Unix/macOS:
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### 2. Frontend (Next.js):
```bash
cd frontend
npm install
npm run dev
```

---

## Running Tests

Run backend automated test suite:

```bash
cd backend
pytest tests/ -v
```
