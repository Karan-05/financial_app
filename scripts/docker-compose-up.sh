#!/bin/bash
set -e

echo "Navigating to the application directory..."
cd /home/ubuntu/FinancialApp

echo "Bringing down existing Docker containers..."
docker-compose down

echo "Starting Docker containers with the latest image..."
docker-compose up -d --build

echo "Docker containers are up and running."
