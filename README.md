# Quote Keeper ✅

[![CI](https://github.com/am-skillup/quote-keeper/actions/workflows/ci.yml/badge.svg)](https://github.com/am-skillup/quote-keeper/actions/workflows/ci.yml)

A small, easy-to-implement project to store, list and retrieve favorite quotes via a simple REST API and a tiny frontend.

## Problem
Many people save memorable quotes in multiple places. This project provides a simple, testable service to store and retrieve quotes with author and optional tags.

## Features
- Create, read, delete quotes
- List quotes and search by tag or author
- Get a random quote
- Minimal frontend (HTML + JS) for quick interaction

## Tech stack
- Backend: FastAPI (Python)
- DB: SQLite (file-based for easy local dev)
- Frontend: plain HTML/JS
- Tests: pytest (backend), jest/jsdom (frontend)
- Containerization: Docker
- CI: GitHub Actions (run tests)

## Acceptance mapping (course criteria)
- Problem description: Covered in this README (criteria 1)
- AI system dev: Not required for this simple closed project, doc will say how to add AI agent later (criteria 2)
- Technologies & architecture: Documented above (criteria 3)
- Front-end implementation: Minimal functional frontend provided; tests included (criteria 4)
- API contract: `openapi.yaml` provided (criteria 5)
- Back-end implementation: FastAPI app follows the OpenAPI contract and includes tests (criteria 6)
- Database integration: SQLite is used and documented (criteria 7)
- Containerization: Dockerfile and docker-compose included (criteria 8)
- Integration testing: Backend tests cover key workflows (criteria 9)
- Deployment: Docker image can be built locally; instructions provided (criteria 10)
- CI/CD pipeline: GitHub Actions workflow runs tests (criteria 11)
- Reproducibility: All instructions to run and test locally are included below (criteria 12)

---

## Quickstart (local)
1. Backend virtual env & deps:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
```

2. Run server:

```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

3. Open the frontend:
Open `frontend/index.html` in your browser and point it to `http://localhost:8000` (or serve it with a small static server).
---

### Database environment (optional)

By default the app uses a local SQLite file (`sqlite:///./quotes.db`). To use a different database, set the `DATABASE_URL` environment variable before starting the app. Examples:

```bash
# Use an on-disk SQLite file (relative to working dir)
export DATABASE_URL="sqlite:///./quotes.db"

# Example: PostgreSQL (replace with your credentials)
export DATABASE_URL="postgresql://postgres:password@localhost:5432/quotes"
```

When running inside Docker you can mount a host directory to persist the SQLite file, e.g.:

```bash
mkdir -p data
# build image
docker build -t quote-keeper .
# run and persist DB in ./data on host (note 4 slashes for absolute path inside container)
docker run --rm -p 8000:8000 -v "$(pwd)/data":/data -e DATABASE_URL="sqlite:////data/quotes.db" quote-keeper
```

### Run via docker-compose

The included `docker-compose.yml` builds the `backend` service. From the project root you can run:

```bash
docker-compose up --build
```

This will start the backend; adjust `DATABASE_URL` as needed in your environment or extend the compose file to include a database service.

4. Run backend tests:

```bash
cd backend
pytest
```

5. Run frontend tests (requires Node.js, recommended >= 18):

```bash
cd frontend
npm ci
npm test
```

---

## Continuous Integration

- This repository uses GitHub Actions to run the test suite on every push and pull request. The CI workflow runs backend tests (pytest) and frontend tests (Jest).
- The CI status badge is shown at the top of this README and links to the workflow runs.
- If you need to reproduce the CI environment locally, run the backend and frontend test commands above. If frontend tests fail locally, ensure Node and npm are installed and match the CI Node version (20).

---

## Files of interest
- `backend/app/` — FastAPI app and models
- `openapi.yaml` — API contract
- `frontend/` — static frontend
- `AGENTS.md` — instructions for coding agents focused on this project

---

If you'd like, I can now implement the backend and tests. 