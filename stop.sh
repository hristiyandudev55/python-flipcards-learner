#!/bin/bash

cd /home/ec2-user/python-flipcards-learner

echo "Stopping Flip Cards application..."

# Kill specific processes from PID files if they exist
if [ -f backend.pid ]; then
    kill $(cat backend.pid) 2>/dev/null || true
    rm backend.pid
    echo "Backend stopped from PID file"
fi

if [ -f frontend/flip-cards-learner/frontend.pid ]; then
    kill $(cat frontend/flip-cards-learner/frontend.pid) 2>/dev/null || true
    rm frontend/flip-cards-learner/frontend.pid
    echo "Frontend stopped from PID file"
fi

# Also kill any other relevant processes that might be running
pkill -f "python -m src.app.main" && echo "Additional backend processes stopped" || true
pkill -f "node.*serve -s dist" && echo "Additional frontend processes stopped" || true

echo "All processes stopped"