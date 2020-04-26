#!/bin/bash

# Install Docker
apt-get update && apt update
apt install -y docker-compose
groupadd docker
gpasswd -a ubuntu docker


mkdir -p /home/ubuntu/jenkins_data
cd /home/ubuntu/capstone/jenkins
docker build --tag=scgerkin/jenkins --rm .
docker run \
--name jenkins \
-p 80:8080 \
-p 50000:50000 \
-v /var/run/docker.sock:/var/run/docker.sock \
-v /home/ubuntu/.aws:/var/jenkins_home/.aws \
-v jenkins_home:/var/jenkins_home \
-d \
scgerkin/jenkins

###### THE FOLLOWING IS NOT SAFE ######
# Refer to this SO post: https://stackoverflow.com/a/33183227/12676661
# This lets the jenkins user in the container access the host docker as if
# it were root. Coincidentally, that means it can run do all kinds of fun stuff
# as if it were the host root. For the purposes of this project, because Jenkins
# is the only thing running on the host, I've decided to go with this solution
# rather than do it properly.
docker exec -u root jenkins /bin/chmod -v a+s $(which docker)
