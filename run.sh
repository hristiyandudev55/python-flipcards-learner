#!/bin/bash

# Start backend server in background
PYTHONPATH=src python -m src.app.main &
BACKEND_PID=$!

# Move to frontend directory and start dev server
cd frontend/flip-cards-learner
npm run dev &
FRONTEND_PID=$!

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID

# Cleanup on script exit
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null" EXIT