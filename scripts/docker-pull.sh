#!/bin/bash
set -e

echo "Pulling the latest Docker image..."
docker pull 051826698008.dkr.ecr.us-east-1.amazonaws.com/financial-app:${IMAGE_TAG}

echo "Docker image pulled successfully."
