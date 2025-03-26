#!/bin/bash

# Set the name of the log file
LOG_FILE="./docker-compose-logs-$(date +%Y%m%d-%H%M%S).log"

# Start docker-compose and capture both stdout and stderr to a log file

cd docker-config 
docker-compose up > "$LOG_FILE" 2>&1 &

# Optionally, display the log file location
echo "Docker Compose logs are being written to: $LOG_FILE"

# (Optional) Wait for services to stabilize
sleep 5

# You can add additional commands here if needed
