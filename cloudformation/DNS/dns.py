#!/usr/bin/env python3
import os
import time
import sys

kube_svc_name = "cyanlb"
stack_name = "CyanDnsRecordSet"
region = "us-east-2"
template_file = "dnsrecordset.yaml"
record_name = "cyan"


def set_args():
  if len(sys.argv) == 1:
    # use defaults above
    return
  elif len(sys.argv) == 6:
    kube_svc_name = sys.argv[1]
    stack_name = sys.argv[2]
    region = sys.argv[3]
    template_file = sys.argv[4]
    record_name = sys.argv[5]
  else:
    raise Exception("Invalid number of arguments.")


def get_hostname() -> str:
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


def create_record(hostname: str, hosted_zone_id: str) -> str:
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
  hostname = get_hostname()
  lb_name = get_lb_name(hostname)
  hosted_zone_id = get_hosted_zone_id(lb_name)
  stack_arn = create_record(hostname, hosted_zone_id)
  await_creation(region, stack_name)
  print(f"http://{record_name}.scgrk.com")


if __name__ == "__main__":
  set_args()
  main()
