MCP example — Quote Keeper

This folder contains a minimal example to show how an MCP-compatible agent (or operator) can be wired to run tests and make changes to this repository. It is intentionally minimal and meant as a starting point for reproducible evaluation.

Files:
- `example_config.yaml` — example MCP plugin configuration that exposes a safe set of workspace tools (run tests, run commands, edit files).
- `run_example.sh` — a small script that documents the flow you'd use to run an MCP server plus the agent for local evaluation.

Notes & recommended steps:
1. Install or run an MCP server that supports registering plugins which expose commands for the agent to call.
2. Register a plugin that allows the agent to: run `pytest` in `/backend`, run `npm test` in `/frontend`, and run `git` commands.
3. Start the MCP server and register the plugin using the `example_config.yaml` as a guide.
4. Start the agent and point it at the MCP server. The agent should be constrained to the repository workspace and a minimal set of privileged actions (no secrets).

Security note: Do not expose any credentials or secrets via the MCP plugin; use repository-hosted secrets (e.g., GitHub Actions secrets) for any remote operations.
