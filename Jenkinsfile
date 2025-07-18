pipeline {
    agent any

    parameters {
        booleanParam(name: 'BUILD_SERVICES',  defaultValue: false, description: 'Build Services module')
        booleanParam(name: 'BUILD_SQL',       defaultValue: false, description: 'Build SQL module')
        booleanParam(name: 'BUILD_METADATA',  defaultValue: false, description: 'Build Metadata module')
        string(name: 'RELEASE', defaultValue: '25.1.0', description: 'Release version tag')
    }

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
                echo "Code checked out from branch: ${env.BRANCH_NAME}"
            }
        }

        stage('Check Selected Components') {
            steps {
                script {
                    if (!params.BUILD_SERVICES && !params.BUILD_SQL && !params.BUILD_METADATA) {
                        echo "No components selected — performing dry run (checkout only)."
                        currentBuild.result = 'SUCCESS'
                        error("Dry run completed — exiting pipeline.")
                    }
                }
            }
        }

        stage('Build Services') {
            when { expression { params.BUILD_SERVICES } }
            steps {
                script {
                    def dateTag = new Date().format('ddMM')
                    echo "Building Services module..."
                    bat "mvn clean package -f backend-webapi/pom.xml -DskipTests"
                    bat "rename backend-webapi\\target\\backend-webapi.jar backend-webapi.${params.RELEASE}.${dateTag}.${BUILD_NUMBER}.jar"
                }
            }
        }

        stage('Build SQL') {
            when { expression { params.BUILD_SQL } }
            steps {
                script {
                    def dateTag = new Date().format('ddMM')
                    echo "Building SQL module..."
                    bat "mvn clean package -f sql-service/pom.xml -DskipTests"
                    bat "rename sql-service\\target\\sql-service.jar sql-service.${params.RELEASE}.${dateTag}.${BUILD_NUMBER}.jar"
                }
            }
        }

        stage('Build Metadata') {
            when { expression { params.BUILD_METADATA } }
            steps {
                script {
                    def dateTag = new Date().format('ddMM')
                    echo "Building Metadata module..."
                    bat "mvn clean package -f metadata-service/pom.xml -DskipTests"
                    bat "rename metadata-service\\target\\metadata-service.jar metadata-service.${params.RELEASE}.${dateTag}.${BUILD_NUMBER}.jar"
                }
            }
        }

        stage('Archive Artifacts') {
            when { expression { params.BUILD_SERVICES || params.BUILD_SQL || params.BUILD_METADATA } }
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