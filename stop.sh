#!/bin/bash

cd /home/ec2-user/python-flipcards-learner

if [ -f backend.pid ]; then
    echo "Stopping backend process..."
    kill $(cat backend.pid) 2>/dev/null || true
    rm backend.pid
    echo "Backend stopped"
else
    echo "No backend PID file found"
fi

if [ -f frontend/flip-cards-learner/frontend.pid ]; then
    echo "Stopping frontend process..."
    kill $(cat frontend/flip-cards-learner/frontend.pid) 2>/dev/null || true
    rm frontend/flip-cards-learner/frontend.pid
    echo "Frontend stopped"
else
    echo "No frontend PID file found"
fi

ps aux | grep -E 'node|python.*app\.main' | grep -v grep