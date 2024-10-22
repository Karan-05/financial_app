#!/bin/bash
set -e

echo "Validating that the Docker containers are running correctly..."

# Example validation: Check if the Django application is accessible
if curl -s http://localhost:8000/ | grep "Welcome"; then
  echo "Validation successful: Application is running."
  exit 0
else
  echo "Validation failed: Application is not running as expected."
  exit 1
fi
