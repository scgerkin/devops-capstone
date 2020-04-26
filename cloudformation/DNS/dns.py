#!/usr/bin/env python3
import os
import time
import sys


def get_hostname(kube_svc_name):
  shell_cmd = """
    kubectl get svc {0} -o yaml \
    | grep \"hostname\" \
    | awk '{{print $3}}'
  """.format(kube_svc_name)
  result = os.popen(shell_cmd).read().strip()
  while not result:
    print("Hostname is not yet ready, waiting 15 seconds...")
    time.sleep(15)
    result = os.popen(shell_cmd).read().strip()
  print("Hostname: {0}".format(result))
  return result


def get_lb_name(hostname):
  result = hostname.split('.')[0].split('-')[0]
  print("LoadBalancerName: {0}".format(result))
  return result


def get_hosted_zone_id(lb_name):
  shell_cmd = """
    aws elb describe-load-balancers \
      --output=text \
      --load-balancer-names={0} \
      --query "LoadBalancerDescriptions[0].CanonicalHostedZoneNameID"
  """.format(lb_name)
  result = os.popen(shell_cmd).read().strip()
  print("CanonicalHostedZoneNameId: {0}".format(result))
  return result


def create_record(stack_name, region, template_file, hostname, hosted_zone_id,
                  record_name):
  shell_cmd = """
    aws cloudformation create-stack \
      --stack-name {0} \
      --region={1} \
      --template-body file://{2} \
      --parameters \
        ParameterKey=Target,ParameterValue={3} \
        ParameterKey=TargetHostedZoneId,ParameterValue={4} \
        ParameterKey=RecordName,ParameterValue={5}
  """.format(stack_name, region, template_file, hostname, hosted_zone_id,
             record_name)
  result = os.popen(shell_cmd).read().strip()
  print("Stack ARN: {0}".format(result))
  return result


def await_creation(region, stack_name):
  shell_cmd = """
    aws cloudformation wait stack-create-complete \
      --region={0} \
      --stack-name {1}
  """.format(region, stack_name)
  print("Will await creation of stack: {0}".format(stack_name))
  os.system(shell_cmd)
  print("Stack creation is complete.")


def main():
  if len(sys.argv) == 1:
    kube_svc_name = "cyanlb-blue"
    stack_name = "CyanDnsRecordSet"
    region = "us-east-2"
    template_file = "dnsrecordset.yaml"
    record_name = "cyan"
  elif len(sys.argv) == 6:
    kube_svc_name = sys.argv[1]
    stack_name = sys.argv[2]
    region = sys.argv[3]
    template_file = sys.argv[4]
    record_name = sys.argv[5]
  else:
    raise Exception("Invalid number of arguments.")

  hostname = get_hostname(kube_svc_name)
  lb_name = get_lb_name(hostname)
  hosted_zone_id = get_hosted_zone_id(lb_name)
  stack_arn = create_record(stack_name, region, template_file, hostname,
                            hosted_zone_id, record_name)
  await_creation(region, stack_name)
  print("http://{0}.scgrk.com".format(record_name))


if __name__ == "__main__":
  main()
