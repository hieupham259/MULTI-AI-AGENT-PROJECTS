#!/bin/bash

# Deploy script for Multi-Agent AI application
# This script builds and starts the Docker container

set -e  # Exit on any error

CONTAINER_NAME="multi-agent-ai"
IMAGE_NAME="multi-agent-ai"
PORT_8501=8501
PORT_9999=9999

echo "Starting deployment of Multi-Agent AI application..."

# Stop and remove existing container if it exists
echo "Checking for existing container..."
if docker ps -a --format 'table {{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    echo "Stopping existing container: ${CONTAINER_NAME}"
    docker stop ${CONTAINER_NAME} || true
    echo "Removing existing container: ${CONTAINER_NAME}"
    docker rm ${CONTAINER_NAME} || true
fi

# Remove existing image if it exists
echo "Checking for existing image..."
if docker images --format 'table {{.Repository}}' | grep -q "^${IMAGE_NAME}$"; then
    echo "Removing existing image: ${IMAGE_NAME}"
    docker rmi ${IMAGE_NAME} || true
fi

# Build the Docker image
echo "Building Docker image: ${IMAGE_NAME}"
docker build -t ${IMAGE_NAME} .

# Run the container
echo "Starting container: ${CONTAINER_NAME}"
docker run -d \
    --name ${CONTAINER_NAME} \
    -p ${PORT_8501}:8501 \
    -p ${PORT_9999}:9999 \
    --restart unless-stopped \
    ${IMAGE_NAME}

# Check if container is running
echo "Checking container status..."
if docker ps --format 'table {{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    echo "Container '${CONTAINER_NAME}' is running successfully!"
    echo "Container details:"
    docker ps --filter name=${CONTAINER_NAME} --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
    echo ""
    echo "Application should be accessible at:"
    echo "   - Port 8501: http://localhost:${PORT_8501}"
    echo "   - Port 9999: http://localhost:${PORT_9999}"
else
    echo "Failed to start container '${CONTAINER_NAME}'"
    echo "Container logs:"
    docker logs ${CONTAINER_NAME}
    exit 1
fi

echo "Deployment completed successfully!"