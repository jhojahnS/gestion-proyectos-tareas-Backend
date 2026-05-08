#!/bin/bash
set -e

: "${AWS_REGION:?AWS_REGION is required}"
: "${IMAGE_URI:?IMAGE_URI is required}"

CONTAINER_NAME="gestion-proyectos-tareas-api"

ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

aws ecr get-login-password --region "$AWS_REGION" \
  | docker login --username AWS \
  --password-stdin "${ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"

echo "Deploying image: $IMAGE_URI"
docker pull "$IMAGE_URI"

if docker inspect "$CONTAINER_NAME" >/dev/null 2>&1; then
  echo "Existing container found. Reading current environment variables..."

  CURRENT_ENV="$(docker inspect "$CONTAINER_NAME" --format='{{range .Config.Env}}{{println .}}{{end}}')"

  CURRENT_DB_HOST="$(echo "$CURRENT_ENV" | grep '^DB_HOST=' | cut -d= -f2- || true)"
  CURRENT_DB_PORT="$(echo "$CURRENT_ENV" | grep '^DB_PORT=' | cut -d= -f2- || true)"
  CURRENT_DB_NAME="$(echo "$CURRENT_ENV" | grep '^DB_NAME=' | cut -d= -f2- || true)"
  CURRENT_DB_USER="$(echo "$CURRENT_ENV" | grep '^DB_USER=' | cut -d= -f2- || true)"
  CURRENT_DB_PASSWORD="$(echo "$CURRENT_ENV" | grep '^DB_PASSWORD=' | cut -d= -f2- || true)"
  CURRENT_USER_IMAGES_BUCKET="$(echo "$CURRENT_ENV" | grep '^USER_IMAGES_BUCKET=' | cut -d= -f2- || true)"

  DB_HOST="${DB_HOST:-$CURRENT_DB_HOST}"
  DB_PORT="${DB_PORT:-$CURRENT_DB_PORT}"
  DB_NAME="${DB_NAME:-$CURRENT_DB_NAME}"
  DB_USER="${DB_USER:-$CURRENT_DB_USER}"
  DB_PASSWORD="${DB_PASSWORD:-$CURRENT_DB_PASSWORD}"
  USER_IMAGES_BUCKET="${USER_IMAGES_BUCKET:-$CURRENT_USER_IMAGES_BUCKET}"
else
  echo "No existing container found. Using environment variables provided by pipeline."
fi

if [ -z "$DB_HOST" ] || [ -z "$DB_PORT" ] || [ -z "$DB_NAME" ] || [ -z "$DB_USER" ] || [ -z "$DB_PASSWORD" ]; then
  echo "ERROR: Missing database environment variables."
  echo "Required: DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD"
  exit 1
fi

echo "Stopping old container if exists..."
docker stop "$CONTAINER_NAME" || true
docker rm "$CONTAINER_NAME" || true

echo "Starting new container..."
docker run -d \
  --name "$CONTAINER_NAME" \
  --restart unless-stopped \
  -p 8000:8000 \
  -e DB_HOST="$DB_HOST" \
  -e DB_PORT="$DB_PORT" \
  -e DB_NAME="$DB_NAME" \
  -e DB_USER="$DB_USER" \
  -e DB_PASSWORD="$DB_PASSWORD" \
  -e USER_IMAGES_BUCKET="$USER_IMAGES_BUCKET" \
  --log-driver json-file \
  --log-opt max-size=10m \
  --log-opt max-file=3 \
  "$IMAGE_URI"

echo "Container deployed successfully."
docker ps