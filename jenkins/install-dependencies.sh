#!/bin/bash

BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}Installing Maven.${NC}"
curl -LO https://apache.claz.org/maven/maven-3/3.6.3/binaries/apache-maven-3.6.3-bin.tar.gz && \
tar xzvf apache-maven-3.6.3-bin.tar.gz && \
rm apache-maven-3.6.3-bin.tar.gz && \
mv apache-maven-3.6.3 /usr/local/apache-maven-3.6.3

echo -e "${BLUE}Installing Docker Client.${NC}"
apt-get update && \
apt-get -y install apt-transport-https \
    ca-certificates \
    curl \
    gnupg2 \
    software-properties-common && \
curl -fsSL https://download.docker.com/linux/$(. /etc/os-release; echo "$ID")/gpg > /tmp/dkey; apt-key add /tmp/dkey && \
add-apt-repository \
    "deb [arch=amd64] https://download.docker.com/linux/$(. /etc/os-release; echo "$ID") \
    $(lsb_release -cs) \
    stable" && \
apt-get update && \
apt-get -y install docker-ce
usermod -a -G docker jenkins

echo -e "${BLUE}Installing pip3 and awscli.${NC}"
apt update -y
apt install python3-pip -y
pip3 install awscli

mkdir -p /var/jenkins_home/.aws
echo -e "[default]\noutput = text" &> /var/jenkins_home/.aws/config

echo -e "${BLUE}Installing eksctl.${NC}"
curl --silent --location "https://github.com/weaveworks/eksctl/releases/download/0.17.0-rc.0/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp
sudo mv /tmp/eksctl /usr/local/bin

echo -e "${BLUE}Installing aws-iam-authenticator.${NC}"
curl -o aws-iam-authenticator https://amazon-eks.s3.us-west-2.amazonaws.com/1.15.10/2020-02-22/bin/linux/amd64/aws-iam-authenticator
chmod +x aws-iam-authenticator
mv aws-iam-authenticator /usr/local/bin

echo -e "${BLUE}Installing kubectl.${NC}"
curl -LO https://storage.googleapis.com/kubernetes-release/release/`curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt`/bin/linux/amd64/kubectl
chmod +x ./kubectl
sudo mv ./kubectl /usr/local/bin/kubectl

echo -e "${BLUE}Finished installing dependencies.${NC}"
