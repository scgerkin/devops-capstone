FROM jenkins/jenkins:lts-jdk11

# Set up our admin account, no need for the wizard
ENV JAVA_OPTS="-Djenkins.install.runSetupWizard=false"

COPY .secret/security.json /var/jenkins_home/security.json
COPY security.groovy /usr/share/jenkins/ref/init.groovy.d/security.groovy
COPY .secret/credentials.json /var/jenkins_home/credentials.json
COPY credentials.groovy /usr/share/jenkins/ref/init.groovy.d/credentials.groovy
COPY jenkins.yaml /var/jenkins_home/jenkins.yaml
COPY install-dependencies.sh /install-dependencies.sh

# Install Dependencies
USER root
RUN chmod +x /install-dependencies.sh
RUN /install-dependencies.sh
# Set Maven's special path
ENV M2_HOME=/usr/local/apache-maven-3.6.3
ENV M2=$M2_HOME/bin
ENV PATH=$PATH:$M2
USER jenkins

# Install Jenkins plugins
COPY plugins.txt /usr/share/jenkins/ref/plugins.txt
RUN /usr/local/bin/install-plugins.sh < /usr/share/jenkins/ref/plugins.txt
