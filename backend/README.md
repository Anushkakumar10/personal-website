# Backend

FastAPI backend scaffold for the Predusk assessment.

Run locally:

1. pipenv install --dev
2. pipenv run uvicorn app.main:app --reload --port 8000

Routes available:
- GET /health
- GET /profile
- PUT /profile
- GET /projects
- GET /skills/top
- GET /skills/search?q=...
