#!/bin/bash

echo "Stopping Flip Cards application..."

# Kill Python backend processes
pkill -f "python -m src.app.main" && echo "Backend stopped" || echo "No backend processes found"

# Kill Node.js frontend processes
pkill -f "node.*serve -s dist" && echo "Frontend stopped" || echo "No frontend processes found"

echo "All processes stopped"