#!/bin/bash

# Get inet IP address from ifconfig output
INET_IP=$(ifconfig | grep -o 'inet [0-9]\+\.[0-9]\+\.[0-9]\+\.[0-9]\+' | awk '{print $2}')

echo "inet IP address: $INET_IP"

# Start FastAPI application with uvicorn
uvicorn app:app --reload --host 0.0.0.0
