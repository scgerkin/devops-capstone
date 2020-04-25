#!/usr/bin/env python3
import os

def get_hostname(kube_svc_name: str) -> str:
  shell_cmd = f"""
    kubectl get svc {kube_svc_name} -o yaml \
    | grep \"hostname\" \
    | awk '{{print $3}}'
  """
  return os.popen(shell_cmd).read().strip()


def get_lb_name(hostname: str) -> str:
  return hostname.split('.')[0].split('-')[0]


def get_hosted_zone_id(lb_name: str) -> str:
  shell_cmd = f"""
    aws elb describe-load-balancers \
      --output=text \
      --load-balancer-names={lb_name}
  """
  return os.popen(shell_cmd).read().strip().split('\t')[2]


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
  # return the stack ARN
  return os.popen(shell_cmd).read().strip()


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
  template_file = "recordset.yaml"
  record_name = "cyan"

  hostname = get_hostname(kube_svc_name)
  lb_name = get_lb_name(hostname)
  hosted_zone_id = get_hosted_zone_id(lb_name)
  stack_arn = create_record(stack_name, region, template_file, hostname,
      hosted_zone_id, record_name)
  await_creation(region, stack_name)


if __name__ == "__main__":
  main()
