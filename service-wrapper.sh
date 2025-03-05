#!/bin/bash

# Source the environment variables
source /home/ec2-user/python-flipcards-learner/.env

# Add poetry to PATH if needed
export PATH=$PATH:$HOME/.local/bin

cd /home/ec2-user/python-flipcards-learner

# Activate Poetry environment
source $(poetry env info --path)/bin/activate

# Clean up any existing processes
if [ -f backend.pid ]; then
    kill $(cat backend.pid) 2>/dev/null || true
    rm backend.pid
fi

if [ -f frontend/flip-cards-learner/frontend.pid ]; then
    kill $(cat frontend/flip-cards-learner/frontend.pid) 2>/dev/null || true
    rm frontend/flip-cards-learner/frontend.pid
fi

# Start backend server with correct Python path
PYTHONPATH=/home/ec2-user/python-flipcards-learner/src python -m src.app.main --host 0.0.0.0 --port 8000 > backend.log 2>&1 &
BACKEND_PID=$!
echo $BACKEND_PID > backend.pid

# Move to frontend directory and build/serve
cd frontend/flip-cards-learner
npm run build
npx serve -s dist -l 5173 > frontend.log 2>&1 &
FRONTEND_PID=$!
echo $FRONTEND_PID > frontend.pid

echo "Application started - Backend PID: $BACKEND_PID, Frontend PID: $FRONTEND_PID"

# Keep the script running to prevent systemd from restarting
tail -f /dev/null