#!/bin/bash
set -e

# Go to the directory where this script is located
cd "$(dirname "$0")"
cd ..

# Accept environment argument: "dev" or "stable"
ENV="${1:-dev}"
ENV_FILE=".env.${ENV}"
COMMON_ENV_FILE=".env.common"

# Check if the env file exists
if [ ! -f "$ENV_FILE" ]; then
  echo "❌ Environment file '$ENV_FILE' not found!"
  exit 1
fi

# Check if the common environment file exists
if [ ! -f "$COMMON_ENV_FILE" ]; then
  echo "❌ Common environment file '$COMMON_ENV_FILE' not found!"
  exit 1
fi

# Load environment variables from both .env.common and .env.{dev|stable}
export $(grep -v '^#' "$COMMON_ENV_FILE" | xargs)  # Load common environment variables
export $(grep -v '^#' "$ENV_FILE" | xargs)         # Load environment-specific variables

# Variables
IMAGE_NAME="${IMAGE_NAME:-coffee_api}"
TAG="${TAG:-$ENV}"
REGISTRY="${REGISTRY:-docker.io}"
COMPOSE_PROJECT_NAME="${COMPOSE_PROJECT_NAME:-coffee_${ENV}}"

# Build Docker image
docker build -t "$IMAGE_NAME:$TAG" ./coffee_api

# Optionally push to registry
# docker push "$REGISTRY/$IMAGE_NAME:$TAG"

# Run Docker Compose with correct project name
docker-compose --env-file "$COMMON_ENV_FILE" --env-file "$ENV_FILE" -p "$COMPOSE_PROJECT_NAME" up -d

echo "✅ Build complete: $IMAGE_NAME:$TAG using environment: $ENV_FILE"
