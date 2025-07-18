pipeline {
    agent any

    parameters {
        booleanParam(name: 'DRY_RUN', defaultValue: false, description: 'Check this for a dry run (only pull code)')
        booleanParam(name: 'BUILD_SERVICES',  defaultValue: false, description: 'Build Services module')
        booleanParam(name: 'BUILD_SQL',       defaultValue: false, description: 'Build SQL module')
        booleanParam(name: 'BUILD_METADATA',  defaultValue: false, description: 'Build Metadata module')
        string(name: 'RELEASE', defaultValue: '1.0.0', description: 'Release version tag')
    }

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
                echo "Code checked out from branch: ${env.BRANCH_NAME}"
            }
        }

        stage('Dry Run Check') {
            when { expression { params.DRY_RUN } }
            steps {
                echo "Dry run selected: Only fetched the latest code & Jenkinsfile."
            }
        }

        stage('Build Selected Components') {
            when { expression { !params.DRY_RUN } }
            steps {
                script {
                    def dateTag = new Date().format('ddMM')

                    // Build Services
                    if (params.BUILD_SERVICES) {
                        echo "Building Services module..."
                        sh "mvn clean package -f backend-webapi/pom.xml -DskipTests"
                        sh "mv backend-webapi/target/backend-webapi.jar backend-webapi.${params.RELEASE}.${dateTag}.${BUILD_NUMBER}.jar"
                    }

                    // Build SQL
                    if (params.BUILD_SQL) {
                        echo "Building SQL module..."
                        sh "mvn clean package -f sql-service/pom.xml -DskipTests"
                        sh "mv sql-service/target/sql-service.jar sql-service.${params.RELEASE}.${dateTag}.${BUILD_NUMBER}.jar"
                    }

                    // Build Metadata
                    if (params.BUILD_METADATA) {
                        echo "Building Metadata module..."
                        sh "mvn clean package -f metadata-service/pom.xml -DskipTests"
                        sh "mv metadata-service/target/metadata-service.jar metadata-service.${params.RELEASE}.${dateTag}.${BUILD_NUMBER}.jar"
                    }
                }
            }
        }

        stage('Archive Artifacts') {
            when { expression { !params.DRY_RUN } }
            steps {
                archiveArtifacts artifacts: '*.jar', fingerprint: true
                echo "Artifacts archived successfully."
            }
        }
    }

    post {
        success {
            echo "Build completed successfully on branch: ${env.BRANCH_NAME}"
        }
        failure {
            echo "Build failed on branch: ${env.BRANCH_NAME}"
        }
    }
}