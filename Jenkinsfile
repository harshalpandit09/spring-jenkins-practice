pipeline {
  agent any

  parameters {
    booleanParam(name: 'BUILD_SERVICES',  defaultValue: false, description: 'Build Services Module')
    booleanParam(name: 'BUILD_SQL',       defaultValue: false, description: 'Build SQL Module')
    booleanParam(name: 'BUILD_METADATA',  defaultValue: false, description: 'Build Metadata Module')
    string(name: 'RELEASE', defaultValue: '1.0.0', description: 'Release version')
  }

  environment {
    MAVEN_HOME = tool name: 'Maven-3.8.5', type: 'maven'
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Build Selected Components') {
      steps {
        script {
          def dateTag = new Date().format('ddMM')

          if (params.BUILD_SERVICES) {
            sh "${MAVEN_HOME}/bin/mvn clean package -f backend-webapi/pom.xml -DskipTests"
            sh "mv backend-webapi/target/backend-webapi.jar backend-webapi.${params.RELEASE}.${dateTag}.${BUILD_NUMBER}.jar"
          }

          if (params.BUILD_SQL) {
            sh "${MAVEN_HOME}/bin/mvn clean package -f sql-service/pom.xml -DskipTests"
            sh "mv sql-service/target/sql-service.jar sql-service.${params.RELEASE}.${dateTag}.${BUILD_NUMBER}.jar"
          }

          if (params.BUILD_METADATA) {
            sh "${MAVEN_HOME}/bin/mvn clean package -f metadata-service/pom.xml -DskipTests"
            sh "mv metadata-service/target/metadata-service.jar metadata-service.${params.RELEASE}.${dateTag}.${BUILD_NUMBER}.jar"
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
}