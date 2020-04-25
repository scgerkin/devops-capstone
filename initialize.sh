#!/usr/bin/env bash

# Create JenkinsBox instance
cd cloudformation
./create.sh JenkinsBox

# Set up initial EKS cluster
cd ../eksctl
eksctl create cluster -f initial-cluster.yaml

# Apply initial deployment and load balance service
cd ../kubectl
kubectl apply -f initial-deployment.yaml
kubectl apply -f initial-lb-svc.yaml

# Set up initial DNS to the load balancer
hostname=$(kubectl get svc cyanlb | grep "hostname" | awk '{print $3}')
while [ hostname == "<pending>"]
do
  wait 30
  hostname=$(kubectl get svc cyanlb | grep "hostname" | awk '{print $3}')
done

cd ../cloudformation/DNS
./dns.py

# TODO: Update aws-auth ConfigMap with Jenkins IAM user
