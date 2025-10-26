#!/bin/bash

CONTAINER_NAME="jenkins-dind"
IMAGE_NAME="jenkins-dind"

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

# Build and run the Jenkins container with Docker-in-Docker support
docker build -t jenkins-dind -f ../Dockerfile.jenkins .
docker run -d --name jenkins-dind \
	--privileged \
	-p 8080:8080 -p 50000:50000 \
	-v /var/run/docker.sock:/var/run/docker.sock \
	-v jenkins_home:/var/jenkins_home \
	jenkins-dind

# Check if container is running
echo "Checking container status..."
docker ps -f name=jenkins-dind

# Retrieve Jenkins logs and get the initial admin password
docker logs jenkins-dind 2>&1 | grep 'Please use the following password to proceed to installation:'