#!groovy

import jenkins.model.*
import hudson.security.*
import jenkins.security.s2m.AdminWhitelistRule
import hudson.security.csrf.DefaultCrumbIssuer
import jenkins.security.s2m.*
import groovy.json.JsonSlurper

def instance = Jenkins.getInstance()

def jsonSlurper = new JsonSlurper()

secretsFile = new File("/var/jenkins_home/security.json")
def secrets = jsonSlurper.parseText(secretsFile.text.trim())

def user = secrets.jenkinsUser
def pass = secrets.jenkinsPass

def hudsonRealm = new HudsonPrivateSecurityRealm(false)
hudsonRealm.createAccount(user, pass)
instance.setSecurityRealm(hudsonRealm)

def strategy = new FullControlOnceLoggedInAuthorizationStrategy()
instance.setAuthorizationStrategy(strategy)
instance.save()

Jenkins.instance.getInjector().getInstance(AdminWhitelistRule.class).setMasterKillSwitch(false)

// set CSRF protection
instance.setCrumbIssuer(new DefaultCrumbIssuer(true))
instance.save()

// Disable JNLP
instance.setSlaveAgentPort(-1)
HashSet<String> newProtocols = new HashSet<>(instance.getAgentProtocols());
newProtocols.removeAll(Arrays.asList(
        "JNLP3-connect", "JNLP2-connect", "JNLP-connect", "CLI-connect"
));
instance.setAgentProtocols(newProtocols);
instance.save()

secretsFile.delete()
