pipeline {
  agent any

  parameters {
    string(name: 'BRANCH',     defaultValue: 'main',  description: 'Git branch to build')
    choice(name: 'COMPONENT',  choices: ['None','Services','SQL','Metadata','All'],
           description: 'Select module to build (None = dry‑run)')
    string(name: 'RELEASE',    defaultValue: '1.0.0',  description: 'Release version tag')
  }

  environment {
    MAVEN_HOME = tool name: 'Maven-3.8.5', type: 'maven'
  }

  stages {
    stage('Checkout & Clean') {
      steps {
        // Pull latest code & Jenkinsfile
        checkout([$class: 'GitSCM',
                  branches: [[name: params.BRANCH]],
                  userRemoteConfigs: [[url: 'https://github.com/harshalpandit09/spring-jenkins-practice.git']]])
        deleteDir()
      }
    }

    stage('Build or Dry‑Run') {
      steps {
        script {
          if (params.COMPONENT == 'None') {
            echo "Dry‑run: only checked out ${params.BRANCH}"
          } else {
            // Map choice → modules
            def map = [
              Services : 'backend-webapi',
              SQL      : 'sql-service',
              Metadata : 'metadata-service',
              All      : 'backend-webapi,sql-service,metadata-service'
            ]
            def toBuild = map[params.COMPONENT].split(',')

            // Build & rename each
            def dateTag = new Date().format('ddMM')
            toBuild.each { mod ->
              sh "${MAVEN_HOME}/bin/mvn clean package -f ${mod}/pom.xml -DskipTests"
              def src = "${mod}/target/${mod}.jar"
              def dst = "${mod}.${params.RELEASE}.${dateTag}.${env.BUILD_NUMBER}.jar"
              sh "mv ${src} ${dst}"
            }
          }
        }
      }
    }

    stage('Archive Artifacts') {
      steps {
        archiveArtifacts artifacts: '*.jar', fingerprint: true
      }
    }
  }

  post {
    success { echo "Build complete: ${params.COMPONENT} @ ${params.BRANCH} (v${params.RELEASE})" }
    failure { echo "Build failed: ${params.COMPONENT} @ ${params.BRANCH}" }
  }
}