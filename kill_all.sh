#!/bin/bash

# Kill backend (uvicorn) process
UVICORN_PID=$(ps aux | grep 'uvicorn main:app' | grep -v grep | awk '{print $2}')
if [ -n "$UVICORN_PID" ]; then
    echo "Stopping backend (uvicorn) with PID: $UVICORN_PID"
    kill $UVICORN_PID
else
    echo "Backend (uvicorn) not found running."
fi

# Kill frontend (npm start) process
NPM_START_PID=$(ps aux | grep 'react-scripts/scripts/start.js' | grep -v grep | awk '{print $2}')
if [ -n "$NPM_START_PID" ]; then
    echo "Stopping frontend (npm start) with PID: $NPM_START_PID"
    kill $NPM_START_PID
else
    echo "Frontend (npm start) not found running."
fi

echo "Attempted to stop all processes."