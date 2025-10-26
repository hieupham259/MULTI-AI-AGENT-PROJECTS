#!/bin/bash

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