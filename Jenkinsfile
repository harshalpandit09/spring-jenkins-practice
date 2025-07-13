pipeline {
    agent any

    parameters {
        string(name: 'BRANCH', defaultValue: 'main', description: 'Git branch to build')
        choice(name: 'COMPONENT', choices: ['ALL', 'Services', 'SQL', 'Metadata'], description: 'Select component to build')
        choice(name: 'CLIENT', choices: ['HSBC', 'JP Morgan', 'DB Bank','Snehal Bank'], description: 'Client name')
        choice(name: 'ENVIRONMENT', choices: ['DEV', 'UAT', 'PROD'], description: 'Target environment')
    }

    environment {
        MAVEN_HOME = tool 'Maven'
        PATH = "${env.MAVEN_HOME}/bin;${env.PATH}" // Use semicolon for Windows
    }

    stages {
        stage('Checkout Code') {
            steps {
                git branch: "${params.BRANCH}", url: 'https://github.com/harshalpandit09/spring-jenkins-practice.git'
            }
        }

        stage('Build with Maven') {
            steps {
                script {
                    def map = [
                        'Services' : 'backend-webapi',
                        'SQL'      : 'sql-service',
                        'Metadata' : 'metadata-service',
                        'ALL'      : 'backend-webapi,sql-service,metadata-service'
                    ]
                    env.COMPONENT_MAP = map[params.COMPONENT]
                }

                bat "mvn clean install -pl \"%COMPONENT_MAP%\" -am"
            }
        }

        stage('Deploy Artifacts') {
            steps {
                bat 'python build_and_deploy.py'
            }
        }

        stage('Post Deploy') {
            steps {
                echo "Build completed and deployed for CLIENT: ${params.CLIENT}, ENV: ${params.ENVIRONMENT}"
            }
        }
    }

    post {
        failure {
            echo "Build failed for CLIENT: ${params.CLIENT} on BRANCH: ${params.BRANCH}"
        }
        success {
            echo "Build & Deployment succeeded!"
        }
    }
}