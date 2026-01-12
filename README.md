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

---

## Deployment

The app is deployed on Render and is publicly available at:

- https://quote-keeper.onrender.com — frontend served at `/`
- Health endpoint: `https://quote-keeper.onrender.com/health` (returns 200 JSON)

The CI includes a smoke test that verifies the deployed service responds at `/` and `/health` after a successful image publish.

---

## Deploy verification ✅

If you want to manually verify the deployed site is serving the frontend and the API:

1. Visit https://quote-keeper.onrender.com — you should see the frontend UI (check page title or that the form is visible).
2. Check the health endpoint:

```bash
curl -sS https://quote-keeper.onrender.com/health | jq
# expected: {"status":"ok","message":"alive"}
```

3. Perform a quick API smoke test (create + list):

```bash
curl -sS -X POST https://quote-keeper.onrender.com/quotes -H "Content-Type: application/json" -d '{"text":"Deploy test","author":"CI","tags":["smoke"]}' | jq
curl -sS https://quote-keeper.onrender.com/quotes | jq
```

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

## Project verification checklist (how to verify each grading criterion) ✅

Use this checklist to verify evidence for each criterion:

1. Problem description
- Verify: `README.md` contains a clear problem statement and feature list.
- Command: open `README.md` and confirm the Problem and Features sections.

2. AI system development (MCP)
- Verify: `AGENTS.md` documents the agent/MCP workflow and permissions and `mcp/` contains example config.
- Command: open `AGENTS.md` and `mcp/example_config.yaml`.

3. Technologies & system architecture
- Verify: `README.md` lists backend, frontend, DB, containerization and CI; architecture explanation present.
- Command: open `README.md` Tech stack section.

4. Front-end implementation
- Verify: `frontend/` contains `index.html`, `main.js`, and tests `frontend/__tests__/ui.test.js` that pass.
- Command: `cd frontend && npm ci && npm test` (CI runs this too).

5. API contract (OpenAPI)
- Verify: `openapi.yaml` lists endpoints and schemas matching backend behavior.
- Command: open `openapi.yaml` and compare with `backend/app/main.py` routes; visit `/docs` on a running instance.

6. Back-end implementation and tests
- Verify: `backend/app/` routes match OpenAPI; `backend/tests/test_api.py` covers core flows and passes.
- Command: `cd backend && pytest` and inspect tests and implementation files.

7. Database integration
- Verify: `backend/app/db.py` supports `DATABASE_URL` and the app runs with default SQLite and can be configured for Postgres.
- Command: start app with `DATABASE_URL` set to a Postgres URL (if available) or run default SQLite locally.

8. Containerization
- Verify: `Dockerfile` and `docker-compose.yml` exist and `docker build` succeeds.
- Command: `docker build -t quote-keeper .` and `docker-compose up --build`.

9. Integration testing
- Verify: backend tests exercise DB and endpoints; smoke tests validate deployed instance.
- Command: `cd backend && pytest`; check CI `smoke-test` job for the deployed site.

10. Deployment
- Verify: a public deployment exists and responds (Render URL documented in README).
- Command: Visit https://quote-keeper.onrender.com and run the smoke-test curl commands above.

11. CI/CD pipeline
- Verify: `.github/workflows/ci.yml` runs tests and publishes images; smoke-test verifies deployed site.
- Command: open the Actions page for the repo and inspect recent workflow run results.

12. Reproducibility
- Verify: README and AGENTS.md provide instructions to set up, run, and test the system locally.
- Command: follow the Quickstart steps in README and AGENTS.md and confirm tests run and app starts.

---

## Continuous Integration

- This repository uses GitHub Actions to run the test suite on every push and pull request. The CI workflow runs backend tests (pytest) and frontend tests (Jest).
- The CI status badge is shown at the top of this README and links to the workflow runs.
- If you need to reproduce the CI environment locally, run the backend and frontend test commands above. If frontend tests fail locally, ensure Node and npm are installed and match the CI Node version (20).
- The CD workflow is handled by Render and deploys automatically after every commit in the main branch of this repo.

---

## Files of interest
- `backend/app/` — FastAPI app and models
- `openapi.yaml` — API contract
- `frontend/` — static frontend
- `AGENTS.md` — instructions for coding agents focused on this project
