#!/bin/bash
# Start Jac Cloud backend (port 8000)
jac serve main.jac &

# Wait 3 seconds for it to start
sleep 3

# Start FastAPI REST API (port 8001)
python server.py
