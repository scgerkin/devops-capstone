#!/usr/bin/env bash

aws cloudformation delete-stack --stack-name JenkinsBox --region=us-east-2
aws cloudformation delete-stack --stack-name CyanDnsRecord --region=us-east-2
eksctl delete cluster Capstone --wait
echo "Done with cleanup"
