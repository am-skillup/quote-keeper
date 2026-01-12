#!/usr/bin/env bash
# Example steps for running an MCP agent workflow locally
# This script is informative and may need adjustment for your MCP server.
set -euo pipefail

echo "1) Start an MCP server (not provided here)."
echo "2) Register the plugin using mcp/example_config.yaml"
echo "   For example: mcpctl register --config mcp/example_config.yaml"

echo "3) Start an agent and point it to the MCP server."
echo "   The agent should be configured to only use the plugin commands above."

echo "4) From the agent you can run 'run-backend-tests' or 'run-frontend-tests' via the plugin."

echo "5) Inspect results and allow the agent to propose edits and commits as needed."

echo "(This script is a guide — replace with commands for your MCP server.)"
