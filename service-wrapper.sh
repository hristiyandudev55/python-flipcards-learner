#!/bin/bash

# Source the environment variables
source /home/ec2-user/python-flipcards-learner/.env

# Add poetry to PATH if needed
export PATH=$PATH:$HOME/.local/bin

# Execute the original script
exec /home/ec2-user/python-flipcards-learner/run.sh
