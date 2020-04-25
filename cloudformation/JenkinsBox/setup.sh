#!/bin/bash

# Install Docker
apt-get update && apt update
apt install -y docker-compose
groupadd docker
gpasswd -a ubuntu docker


mkdir -p /home/ubuntu/.kube
mkdir -p /home/ubuntu/jenkins_data
cd /home/ubuntu/capstone/.jenkins
docker build --tag=scgerkin/jenkins --rm .
docker run \
--name jenkins \
-p 80:8080 \
-p 50000:50000 \
-v /var/run/docker.sock:/var/run/docker.sock \
-v /home/ubuntu/.aws:/var/jenkins_home/.aws \
-v jenkins_home:/var/jenkins_home \
-d \
scgerkin/jenkins
