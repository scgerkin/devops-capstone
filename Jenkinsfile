pipeline {
  environment {
    appName = ""
    version = ""
    registry = "scgerkin/"
    buildId = "$currentBuild.fullDisplayName"
    alertMsg = ""
    registryCreds = 'docker'
    endpoint = ""
    imageName = ""
    featureBranchName = "feature"
    masterBranchName = "master"
  }
  agent any
  stages {
    stage ('Initialize with clean target dir') {
      steps {
        sh 'mvn clean'
      }
    }
    stage ('Lint') {
      steps {
        sh 'mvn checkstyle:check'
      }
    }
    stage ('Run unit tests') {
      steps {
        sh 'mvn test'
      }
    }
    stage ('Package') {
      steps {
        sh 'mvn package -DskipTests'
      }
    }
    stage ('SpotBugs') {
      steps {
        sh 'mvn spotbugs:check'
      }
    }
    stage ('PMD Source Code Analyzer') {
      steps {
        sh 'mvn pmd:check'
      }
    }
    stage ('Set versioning') {
      steps {
        script {
          appName = sh(returnStdout: true, script: "mvn help:evaluate -Dexpression=project.artifactId -q -DforceStdout")
          version = sh(returnStdout: true, script: "mvn help:evaluate -Dexpression=project.version -q -DforceStdout")
          registry += appName
          imageName = registry + ":" + version
        }
      }
    }
    stage ('Feature Test Tag Docker') {
      when { branch featureBranchName }
      steps {
        script {
          //fixme: this screws up versioning for deployment, hack fixed
          imageName += "-TestBuild"
        }
      }
    }
    stage ('Push Docker Image') {
      steps {
        script {
          image = docker.build(
            imageName,
            "--build-arg jarName=" + appName + "-" + version + ".jar ."
          )
          docker.withRegistry('', registryCreds) { image.push() }
        }
      }
    }
    stage ('Feature Tests Setup') {
      when { branch featureBranchName }
      steps {
        echo 'Performing Feature testing.'
        sh 'rm -rf ~/.kube'
        sh 'eksctl create cluster -f eksctl/test-cluster.yaml'
        //fixme: this fixes the hack above
        script { version += "-TestBuild" }
        sh "sed -i \"s/<APPVERSION>/$version/g\" kubectl/test-deployment.yaml"
        sh 'kubectl apply -f kubectl/test-deployment.yaml'
        //fixme: waiting hostname, this is super hacky
        sh 'sleep 60'
        script {
          endpoint = sh(returnStdout: true,
            script: "kubectl get svc cyanlb-test -o yaml | grep \"hostname\" | awk '{print \$3}'")
          endpoint = "Endpoint: http://" + endpoint
          echo endpoint
        }
      }
    }
    stage ('Destroy test resources') {
      when { branch featureBranchName }
      steps {
        script {
          alertMsg = "Awaiting input: Clean/Delete test cluster?"
          withAWS(region:'us-east-1',credentials:'aws-static') {
          snsPublish(
            topicArn: "arn:aws:sns:us-east-1:854235326474:GithubRepoPushActions",
            subject: "Pipeline Event",
            message: alertMsg)
          }
        }
        input(message: "Clean/Delete test cluster?")
        sh 'kubectl delete -f kubectl/test-deployment.yaml'
        //fixme: waiting on pods to drain, this is a hack
        sh 'sleep 60'
        sh 'eksctl delete cluster FeatureTest'
      }
    }
    stage ('Green deployment') {
      when { branch masterBranchName }
      steps {
        sh 'rm -rf ~/.kube'
        sh 'aws eks --region us-east-2 update-kubeconfig --name Capstone'
        sh 'eksctl create nodegroup -f eksctl/secondary-ng.yaml'
        sh "sed -i \"/image:/c\\        image: $imageName\" kubectl/secondary-deployment.yaml"
        sh 'kubectl apply -f kubectl/secondary-deployment.yaml'
        sh 'chmod +x cloudformation/DNS/dns.py'
        sh "./cloudformation/DNS/dns.py 'cyanlb-green' 'GreenDnsRecordSet' 'us-east-2' 'cloudformation/DNS/dnsrecordset.yaml' 'cyan-green'"
      }
    }
    stage ('Switch over LB') {
      when { branch masterBranchName }
      steps {
        script {
          alertMsg = "Awaiting input: Deploy Green version to Production environment?"
          withAWS(region:'us-east-1',credentials:'aws-static') {
            snsPublish(
              topicArn: "arn:aws:sns:us-east-1:854235326474:GithubRepoPushActions",
              subject: "Pipeline Event",
              message: alertMsg)
          }
        }
        input(message: "Deploy Green version to Production environment?")
        sh "sed -i \"/image:/c\\        image: $imageName\" kubectl/initial-deployment.yaml"
        sh 'kubectl apply -f kubectl/initial-deployment.yaml'
        sh 'aws cloudformation delete-stack --stack-name GreenDnsRecordSet --region=us-east-2'
      }
    }
    stage ('Update Lts Docker Image') {
      when { branch masterBranchName }
      steps {
        script {
          alertMsg = "Pipeline Awaiting Input\n" + "BuildId: " + buildId + "\n" + "ArtifactId: " + appName + "\n" + "Version: " + version + "\n"
          withAWS(region:'us-east-1',credentials:'aws-static') {
          snsPublish(
            topicArn: "arn:aws:sns:us-east-1:854235326474:GithubRepoPushActions",
            subject: "Pipeline Event",
            message: alertMsg)
          }
        }
        script {
          input(message: "Transition Green deployment to Master Track?" )
          sh 'kubectl delete -f kubectl/secondary-deployment.yaml'
          //fixme: hack
          sh 'sleep 60'
          sh 'eksctl delete nodegroup -f eksctl/secondary-ng.yaml --approve'
          docker.withRegistry('', registryCreds) { image.push("lts") }
        }
      }
    }
  }
  post {
    always {
      sh 'mvn clean'
      sh "docker rmi $registry:$version"
    }
    failure {
      script {
        alertMsg = "Failed Build.\n" + "BuildId: " + buildId + "\n" + "ArtifactId: " + appName + "\n" + "Version: " + version + "\n"
      }
      withAWS(region:'us-east-1',credentials:'aws-static') {
        snsPublish(
          topicArn: "arn:aws:sns:us-east-1:854235326474:GithubRepoPushActions",
          subject: "Pipeline Failure",
          message: alertMsg)
      }
    }
    success {
      script {
        alertMsg = "Successful Build.\n" + "BuildId: " + buildId + "\n" + "ArtifactId: " + appName + "\n" + "Version: " + version + "\n"
        withAWS(region:'us-east-1',credentials:'aws-static') {
          snsPublish(
            topicArn: "arn:aws:sns:us-east-1:854235326474:GithubRepoPushActions",
            subject: "Successful Pipeline Build",
            message: alertMsg)
        }
      }
    }
  }
}
