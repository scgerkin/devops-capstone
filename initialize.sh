#!/usr/bin/env bash

alert () {
  BLUE='\033[0;34m'
  NC='\033[0m'
  echo -e "${BLUE}$1${NC}"
}

# Create JenkinsBox instance
alert "Creating Jenkins machine..."
cd cloudformation
./create.sh JenkinsBox

# Set up initial EKS cluster
alert "Setting up initial EKS cluster..."
cd ../eksctl
eksctl create cluster -f initial-cluster.yaml

# Apply initial deployment and load balance service
alert "Setting up initial deployment and load balancer..."
cd ../kubectl
kubectl apply -f initial-deployment.yaml
kubectl apply -f initial-lb-svc.yaml

# Set up initial DNS to the load balancer
alert "Setting up DNS record set for load balancer..."
cd ../cloudformation/DNS
./dns.py

# TODO: Update aws-auth ConfigMap with Jenkins IAM user
