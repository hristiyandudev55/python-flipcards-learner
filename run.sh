#!/bin/bash

# Ensure we're in the project root directory
cd /home/ec2-user/python-flipcards-learner

# Activate Poetry environment - this is critical
source $(poetry env info --path)/bin/activate

# Start backend server with correct Python path
PYTHONPATH=/home/ec2-user/python-flipcards-learner/src python -m src.app.main --host 0.0.0.0 --port 8000 > backend.log 2>&1 &
BACKEND_PID=$!
echo $BACKEND_PID > backend.pid

# Move to frontend directory and start dev server
cd frontend/flip-cards-learner
npm run build  # Build for production instead of dev
npx serve -s dist -l 5173 > frontend.log 2>&1 &
FRONTEND_PID=$!
echo $FRONTEND_PID > frontend.pid

echo "Application started - Backend PID: $BACKEND_PID, Frontend PID: $FRONTEND_PID"