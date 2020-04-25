stackName=$1
aws cloudformation update-stack --stack-name $stackName --region=us-east-2 --template-body file://$stackName/stack.yaml --parameters file://.secrets/$stackName.json --capabilities "CAPABILITY_IAM" "CAPABILITY_NAMED_IAM"
