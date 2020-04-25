#!/usr/bin/env python3
import os
import time

def get_hostname(kube_svc_name: str) -> str:
  shell_cmd = f"""
    kubectl get svc {kube_svc_name} -o yaml \
    | grep \"hostname\" \
    | awk '{{print $3}}'
  """
  result = os.popen(shell_cmd).read().strip()
  while not result:
    print("Hostname is not yet ready, waiting 15 seconds...")
    time.sleep(15)
    result = os.popen(shell_cmd).read().strip()
  print(f"Hostname: {result}")
  return result


def get_lb_name(hostname: str) -> str:
  result = hostname.split('.')[0].split('-')[0]
  print(f"LoadBalancerName: {result}")
  return result


def get_hosted_zone_id(lb_name: str) -> str:
  shell_cmd = f"""
    aws elb describe-load-balancers \
      --output=text \
      --load-balancer-names={lb_name} \
      --query "LoadBalancerDescriptions[0].CanonicalHostedZoneNameID"
  """
  result = os.popen(shell_cmd).read().strip()
  print(f"CanonicalHostedZoneNameId: {result}")
  return result


def create_record(stack_name: str,
                  region: str,
                  template_file: str,
                  hostname: str,
                  hosted_zone_id: str,
                  record_name: str) -> str:
  shell_cmd = f"""
    aws cloudformation create-stack \
      --stack-name {stack_name} \
      --region={region} \
      --template-body file://{template_file} \
      --parameters \
        ParameterKey=Target,ParameterValue={hostname} \
        ParameterKey=TargetHostedZoneId,ParameterValue={hosted_zone_id} \
        ParameterKey=RecordName,ParameterValue={record_name}
  """
  result = os.popen(shell_cmd).read().strip()
  print(f"Stack ARN: {result}")
  return result


def await_creation(region: str, stack_name: str):
  shell_cmd = f"""
    aws cloudformation wait stack-create-complete \
      --region={region} \
      --stack-name {stack_name}
  """
  print(f"Will await creation of stack: {stack_name}")
  os.system(shell_cmd)
  print("Stack creation is complete.")


def main():
  kube_svc_name = "cyanlb"
  stack_name = "CyanDnsRecordSet"
  region = "us-east-2"
  template_file = "dnsrecordset.yaml"
  record_name = "cyan"

  hostname = get_hostname(kube_svc_name)
  lb_name = get_lb_name(hostname)
  hosted_zone_id = get_hosted_zone_id(lb_name)
  stack_arn = create_record(stack_name, region, template_file, hostname,
      hosted_zone_id, record_name)
  await_creation(region, stack_name)


if __name__ == "__main__":
  main()
