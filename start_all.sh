#!/bin/bash

# Start the backend
echo "Starting backend..."
cd backend
.venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000 > backend_startup.log 2>&1 &
BACKEND_PID=$!
cd ..

# Start the frontend
echo "Starting frontend..."
cd frontend
npm start &
FRONTEND_PID=$!
cd ..

echo "Backend (PID: $BACKEND_PID) and Frontend (PID: $FRONTEND_PID) started in the background."
echo "You can access the frontend at http://localhost:3000/"

# Optional: To stop them later, you can use: kill $BACKEND_PID $FRONTEND_PID