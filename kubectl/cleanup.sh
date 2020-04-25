#!/usr/env/bin bash

kubectl delete -f initial-deployment.yaml
kubectl delete -f secondary-deployment.yaml
kubectl delete -f lb-initial-svc.yaml
kubectl delete -f lb-second-svc.yaml
