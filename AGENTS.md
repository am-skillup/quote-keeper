# Agent Instructions — Quote Keeper 🔧

This file contains concise instructions for coding agents (or assistants) focused on the Quote Keeper project. Use this to scope the agent's actions and provide the context required to implement, test and extend features.

## Repo location
- Project root: `/`
- Backend app: `/backend/app`
- OpenAPI: `/openapi.yaml`
- Frontend: `/frontend`
- Tests: `/backend/tests` and `/frontend/__tests__`

## How to run locally
- Backend (dev):
  - Create venv, install: `pip install -r backend/requirements.txt`
  - Run: `uvicorn app.main:app --reload --port 8000`
  - API docs: `http://localhost:8000/docs`
- Frontend:
  - Open `frontend/index.html` in browser or serve statically and set `API_BASE` to backend URL
- Tests:
  - Backend: `cd backend && pytest`
  - Frontend: `cd frontend && npm ci && npm test`

## API summary (key endpoints)
- POST /quotes — create a quote {text, author, tags}
- GET /quotes — list quotes, optional query params `author` and `tag`
- GET /quotes/{id} — get quote by id
- GET /quotes/random — get a random quote
- DELETE /quotes/{id} — delete a quote

## Agent permissions and constraints
- Allowed: modify files under `/*`, add tests, run unit/integration tests, and update docs.
- Not allowed: change files outside `/` without explicit instruction.
- Prefer small, test-backed changes. Create failing tests first if behavior change is non-trivial.

## Typical tasks & how the agent should approach them
1. Add new field to Quote (e.g., `source`):
   - Add field to `models.py` and update Pydantic/SQLModel models
   - Update `openapi.yaml`
   - Add and run backend tests that assert creation and retrieval
   - Update `frontend` render & tests
2. Add search by tag/author improvements:
   - Add new query behavior to `main.py`, write tests for filtering
   - Update `openapi.yaml` if necessary
3. Implement pagination:
   - Add `limit` and `offset` query params
   - Add tests covering pagination
   - Update docs & OpenAPI
4. Fix bug in API: reproduce via test, implement fix, run tests

## Example unit/integration tests to add
- Ensure `POST /quotes` rejects missing `text` field
- Test list endpoint pagination and filtering combination
- Test backend returns 404 for random when no quotes exist

## When you finish a change
- Ensure all tests pass locally (`pytest` and `npm test`)
- Add or update README if behavior or requirements changed
- Open a PR with a clear description and link to failing/passing tests

## MCP & agent workflow notes

This project documents how an MCP-compatible agent can assist with development. To achieve the full credit for AI-assisted development in the project rubric, we record how MCP was used and how to run a similar workflow locally:

- What we used the agent for:
  - Running tests and reporting failures (backend pytest and frontend jest)
  - Making small code edits and creating test-driven commits
  - Updating docs (README, AGENTS.md) and CI workflow fixes
- How to run an MCP-like agent locally (example outline):
  1. Install an MCP server and register a plugin that exposes the repository workspace and a safe set of tools (run tests, run commands, edit files).
  2. Use the agent to run tests (`pytest` / `npm test`) and inspect failing outputs.
  3. Allow the agent to propose edits and generate commits; review and approve changes before pushing.

Notes:
- AGENTS.md describes the permissions and constraints an agent should follow (modify files inside the repo, add tests, run tests, etc.).
- If you want, I can add a short `mcp/` folder with example server config and a small script that demonstrates how to wire the agent to run the project's test commands for reproducible evaluation.


---

If you want, I can now implement additional features or open a PR with the current scaffold. 