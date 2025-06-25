#!/bin/bash
set -e

# Go to the directory where this script is located
cd "$(dirname "$0")"
cd ..

# Accept environment argument: "dev" or "stable"
ENV="${1:-dev}"
ENV_FILE=".env.${ENV}"
COMMON_ENV_FILE=".env.common"
MASTER_ENV_FILE="master.env"

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

sort -u -t '=' -k 1,1 "$COMMON_ENV_FILE" "$ENV_FILE" | grep -v '^$\|^\s*\#' > "$MASTER_ENV_FILE"

# Load environment variables from both .env.common and .env.{dev|stable}
set -o allexport
source "$MASTER_ENV_FILE"
set +o allexport

# Variables
IMAGE_NAME="${IMAGE_NAME:-coffee_api}"
TAG="${TAG:-$ENV}"
REGISTRY="${REGISTRY:-docker.io}"
COMPOSE_PROJECT_NAME="${COMPOSE_PROJECT_NAME:-coffee_${ENV}}"

# Build Docker image
docker build -t "$IMAGE_NAME:$TAG" ./coffee_api

# Optionally push to registry
# docker push "$REGISTRY/$IMAGE_NAME:$TAG"

# Cleanup based on TAG
echo "🧹 Cleaning up old containers for project: $COMPOSE_PROJECT_NAME"
if [ "$TAG" = "dev" ]; then
  echo "⚠️ Dev environment — removing volumes"
  docker compose --project-name "$COMPOSE_PROJECT_NAME" \
    --env-file "$MASTER_ENV_FILE" \
    down --volumes --remove-orphans
else
  echo "🔒 Stable environment — preserving volumes"
  docker compose --project-name "$COMPOSE_PROJECT_NAME" \
    --env-file "$MASTER_ENV_FILE" \
    down --remove-orphans
fi

echo "🌐 API_PORT resolved to: $API_PORT"

echo "🧾 Validating docker-compose config:"
docker compose --project-name "$COMPOSE_PROJECT_NAME" \
  --env-file "$MASTER_ENV_FILE" config

# Run Docker Compose with correct project name
docker compose --project-name "$COMPOSE_PROJECT_NAME" \
  --env-file "$MASTER_ENV_FILE" \
  up -d

echo "✅ Build complete: $IMAGE_NAME:$TAG using environment: $ENV_FILE"

echo "🌟 Coffee API is live on http://localhost:$API_PORT"
echo "📊 PGAdmin is live on http://localhost:8082"

