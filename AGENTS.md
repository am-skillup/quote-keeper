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

## MCP & agent workflow (project-specific)

This project uses an MCP-style workflow (an MCP-compatible server + an agent) to assist with development tasks in a controlled, auditable way. The agent was used to run tests, execute workspace commands, propose code edits, and create commits; a human reviewed changes and merged them.

What the agent is allowed to do in this repository
- Run test suites and collect results:
  - Backend: `cd backend && pytest -q`
  - Frontend: `cd frontend && npm ci && npm test --silent`
- Build and test container images:
  - Build: `docker build -t quote-keeper .`
  - Run test container: `docker run -d --name quote-keeper-test -p 8000:8000 -v "$(pwd)/data":/data -e DATABASE_URL="sqlite:////data/quotes.db" quote-keeper`
  - Stop & remove: `docker stop quote-keeper-test && docker rm quote-keeper-test`
- Make small code edits, run linters, add tests, and create commits (human approval required before merge/push to `main` by policy)
- Push changes to a feature branch and open PRs (recommended workflow)

Exact workspace commands that should be exposed via an MCP plugin
- `run-backend-tests`: `cd backend && pytest -q`
- `run-frontend-tests`: `cd frontend && npm ci && npm test --silent`
- `build-docker`: `docker build -t quote-keeper .`
- `run-docker-test`: `docker run -d --name quote-keeper-test -p 8000:8000 -v "$(pwd)/data":/data -e DATABASE_URL="sqlite:////data/quotes.db" quote-keeper`
- `stop-docker-test`: `docker stop quote-keeper-test && docker rm quote-keeper-test`
- `git-status`: `git status --porcelain`
- `git-create-commit`: a workflow that stages, commits, and pushes to a branch (agent should request human approval before pushing to main)

Security & policy guidance (important)
- The agent must be restricted by policy to a minimal set of allowed commands and file paths (see `mcp/example_config.yaml` which lists allowed paths). Typical allowed paths include `backend/**`, `frontend/**`, `README.md`, `AGENTS.md`, and `.github/workflows/**`.
- Do not expose secrets through the agent. Use repository-hosted secrets (e.g., GitHub Actions secrets) for any remote publish operations (e.g., pushing images to GHCR).
- Require human approval (pull requests) for any change that will be merged to `main` or that publishes artifacts (images). For publishing to registries (GHCR), require an explicit, reviewable action and a separate approval step.

How to reproduce this workflow locally
1. Install an MCP server or tooling that supports registering plugins exposing limited workspace commands (see vendor docs for your MCP server).
2. Register a plugin using `mcp/example_config.yaml` as the plugin manifest; the plugin should expose the commands above and enforce path restrictions.
3. Start an agent and point it at the MCP server. From the agent UI or CLI you can run `run-backend-tests`, `run-frontend-tests`, `build-docker`, etc.
4. Agent proposes edits as commits; review them and open a PR for human review and merge.

Files in this repo that help reproduce the flow
- `mcp/example_config.yaml` — example plugin manifest used to register the commands above
- `mcp/run_example.sh` — short script describing the local steps for registering the plugin and running an agent command

If you want, I can add a small `mcp/` integration example that runs the tests and produces a sample artifact in a disposable environment — but note that running an MCP server is specific to the tooling you choose and may require additional local setup (TLS, auth, etc.).

---

If you want, I can now implement additional features or open a PR with the current scaffold. 