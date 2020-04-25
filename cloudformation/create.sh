#!/usr/bin/env bash

stackName=$1
aws cloudformation create-stack \
  --stack-name $stackName \
  --region=us-east-2 \
  --template-body file://$(pwd)/$stackName/stack.yaml \
  --parameters file://$(pwd)/.secrets/$stackName.json \
  --capabilities "CAPABILITY_IAM" "CAPABILITY_NAMED_IAM"

echo "Will wait for stack status 'CREATE_COMPLETE'. No output will be written while waiting."
echo "Alert will be posted once status is reached."
echo "This can be safely exited with SIGINT (CTRL+C) without affecting creation."
aws cloudformation wait stack-create-complete --stack-name $stackName --region=us-east-2
echo "Stack '$stackName' is created."
