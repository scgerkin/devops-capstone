import jenkins.model.*
import com.cloudbees.plugins.credentials.*
import com.cloudbees.plugins.credentials.domains.*
import com.cloudbees.plugins.credentials.common.*
import com.cloudbees.plugins.credentials.impl.*
import com.cloudbees.jenkins.plugins.awscredentials.AWSCredentialsImpl
import hudson.util.Secret
import org.jenkinsci.plugins.plaincredentials.impl.StringCredentialsImpl
import groovy.json.JsonSlurper

domain = Domain.global()
store = Jenkins.instance.getExtensionList('com.cloudbees.plugins.credentials.SystemCredentialsProvider')[0].getStore()

secretsFile = new File("/var/jenkins_home/credentials.json")
def jsonSlurper = new JsonSlurper()
def secrets = jsonSlurper.parseText(secretsFile.text.trim())

awsCredentials = new AWSCredentialsImpl(
    CredentialsScope.GLOBAL,
    "aws-static",
    secrets.awsAccessKey,
    secrets.awsSecretKey,
    "AWS S3 credentials"
)
store.addCredentials(domain, awsCredentials)

githubAccessToken = new StringCredentialsImpl(
    CredentialsScope.GLOBAL,
    "github",
    "Github access token",
    Secret.fromString(secrets.githubKey)
)
store.addCredentials(domain, githubAccessToken)

githubCredentials = new UsernamePasswordCredentialsImpl(
  CredentialsScope.GLOBAL,
  "github-acct",
  "GitHub credentials",
  secrets.githubUsername,
  secrets.githubKey
)
store.addCredentials(domain, githubCredentials)

dockerhubCredentials = new UsernamePasswordCredentialsImpl(
  CredentialsScope.GLOBAL,
  "docker",
  "Docker Hub credentials",
  secrets.dockerhubUsername,
  secrets.dockerhubKey
)
store.addCredentials(domain, dockerhubCredentials)

// purge initial setup credential file
secretsFile.delete()
