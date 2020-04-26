#!/usr/bin/env python3
import os
import yaml

sh = "kubectl get cm -n kube-system aws-auth -o yaml"
config = yaml.load(os.popen(sh), Loader=yaml.FullLoader)

accountid = ''
with open('.secrets/accountid', 'r') as f:
  accountid = f.read().strip()

config['data']['mapUsers'] = f"""
  - userarn: arn:aws:iam::{accountid}:user/jenkins
    username: jenkins
    groups:
      - system:masters
  - userarn: arn:aws:iam::{accountid}:/user/devbox
    username: devbox
    groups:
      - system:masters
"""

with open('config.yaml', 'w') as f:
  yaml.dump(config, f, default_flow_style=False)

sh = "kubectl apply -f config.yaml"
os.system(sh)
os.remove('config.yaml')
