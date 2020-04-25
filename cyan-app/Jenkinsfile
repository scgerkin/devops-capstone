pipeline {
  environment {
    appName = ""
    version = ""
    registry = ""
    buildId = "$currentBuild.fullDisplayName"
    successMsg = ""
    registryCreds = 'docker'
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
    stage ('Compile Sources') {
      steps {
        sh 'mvn compile'
      }
    }
    stage ('Compile Test Sources') {
      steps {
        sh 'mvn test-compile'
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
    stage ('Build Docker image') {
      steps {
        script {
          appName = sh(returnStdout: true, script: "mvn help:evaluate -Dexpression=project.artifactId -q -DforceStdout")
          version = sh(returnStdout: true, script: "mvn help:evaluate -Dexpression=project.version -q -DforceStdout")
          registry = "scgerkin/" + appName
          image = docker.build(registry + ":" + version, "--build-arg jarName=" + appName + "-" + version + ".jar .")
          docker.withRegistry('', registryCreds) {
            image.push()
          }
        }
      }
    }
  }
  post {
    always {
      sh 'mvn clean'
      sh "docker rmi $registry:$version"
    }
    success {
      script {
        successMsg = "Successful Build.\n" + "BuildId: " + buildId + "\n" + "ArtifactId: " + appName + "\n" + "Version: " + version + "\n"
      }
      withAWS(region:'us-east-1',credentials:'aws-static') {
        snsPublish(
          topicArn: "arn:aws:sns:us-east-1:854235326474:GithubRepoPushActions",
          subject: "Successful Pipeline Build",
          message: successMsg)
      }
    }
  }
}
