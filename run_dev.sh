#!/bin/bash
# This script provides a single, reliable command to start the application.
# It ensures that both the backend and frontend services are started correctly
# from the project root, avoiding common issues with relative paths.

# Exit immediately if a command exits with a non-zero status.
set -e

# Get the absolute path of the directory containing this script.
PROJECT_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

BACKEND_DIR="$PROJECT_ROOT/backend"
FRONTEND_DIR="$PROJECT_ROOT/frontend"

# --- Prerequisite Checks ---
if [ ! -f "$BACKEND_DIR/.env" ]; then
    echo "Error: .env file not found in backend directory."
    echo "Please create a .env file in the backend directory with your Alpaca API keys."
    exit 1
fi

if [ ! -f "$BACKEND_DIR/.venv/bin/python" ]; then
    echo "Error: Backend python virtual environment not found."
    echo "Please run the setup script or create it manually."
    exit 1
fi

if [ ! -d "$FRONTEND_DIR/node_modules" ]; then
    echo "Error: Frontend dependencies (node_modules) not found."
    echo "Please run 'npm install' in the 'frontend' directory."
    exit 1
fi

# --- Service Execution ---
# Use concurrently to run both services.
# It provides clear, prefixed output for each service.
# We run it from the frontend directory to leverage the existing dependency.
cd "$FRONTEND_DIR"

echo "--- Starting Backend and Frontend Services ---"
# The backend command is now relative to the project root, making it more stable.
# The frontend command remains the same.
npx concurrently \
  --names "BACKEND,FRONTEND" \
  --prefix-colors "bgBlue.bold,bgMagenta.bold" \
  "cd '$BACKEND_DIR' && source ./.venv/bin/activate && uvicorn main:app --host 0.0.0.0 --port 8000" \
  "npm start"

