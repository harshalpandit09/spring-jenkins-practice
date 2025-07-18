pipeline {
    agent any

    parameters {
        booleanParam(name: 'BUILD_SERVICES',  defaultValue: false, description: 'Build Services module')
        booleanParam(name: 'BUILD_SQL',       defaultValue: false, description: 'Build SQL module')
        booleanParam(name: 'BUILD_METADATA',  defaultValue: false, description: 'Build Metadata module')
        string(name: 'RELEASE', defaultValue: '25.1.0', description: 'Release version tag')
    }

    environment {
        DATE_TAG    = "${new Date().format('ddMM')}"
        BUILD_TAG   = "${params.RELEASE}.${new Date().format('ddMM')}.${env.BUILD_NUMBER}"
        RELEASE_DIR = "Builds\\${params.RELEASE}"
        MANIFEST    = "Builds\\${params.RELEASE}\\build_manifest.txt"
    }

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
                echo "Code checked out from branch: ${env.BRANCH_NAME}"
            }
        }

        stage('Build Services') {
            when { expression { params.BUILD_SERVICES } }
            steps {
                script {
                    echo "Building Services module..."
                    bat "if not exist ${RELEASE_DIR} mkdir ${RELEASE_DIR}"
                    bat "mvn clean package -f backend-webapi/pom.xml -DskipTests"
                    bat """
                        cd backend-webapi\\target
                        rename backend-webapi-0.0.1-SNAPSHOT.jar backend-webapi.${BUILD_TAG}.jar
                        move backend-webapi.${BUILD_TAG}.jar ..\\..\\${RELEASE_DIR}
                    """
                }
            }
        }

        stage('Build SQL') {
            when { expression { params.BUILD_SQL } }
            steps {
                script {
                    echo "Building SQL module..."
                    bat "if not exist ${RELEASE_DIR} mkdir ${RELEASE_DIR}"
                    bat "mvn clean package -f sql-service/pom.xml -DskipTests"
                    bat """
                        cd sql-service\\target
                        rename sql-service-0.0.1-SNAPSHOT.jar sql-service.${BUILD_TAG}.jar
                        move sql-service.${BUILD_TAG}.jar ..\\..\\${RELEASE_DIR}
                    """
                }
            }
        }

        stage('Build Metadata') {
            when { expression { params.BUILD_METADATA } }
            steps {
                script {
                    echo "Building Metadata module..."
                    bat "if not exist ${RELEASE_DIR} mkdir ${RELEASE_DIR}"
                    bat "mvn clean package -f metadata-service/pom.xml -DskipTests"
                    bat """
                        cd metadata-service\\target
                        rename metadata-service-0.0.1-SNAPSHOT.jar metadata-service.${BUILD_TAG}.jar
                        move metadata-service.${BUILD_TAG}.jar ..\\..\\${RELEASE_DIR}
                    """
                }
            }
        }

        stage('Update Manifest') {
            when { expression { params.BUILD_SERVICES || params.BUILD_SQL || params.BUILD_METADATA } }
            steps {
                script {
                    echo "Rebuilding manifest file in ${MANIFEST}"
                    // Delete old manifest
                    bat "del /Q ${MANIFEST} || echo No old manifest"
                    // Generate new manifest
                    bat """
                        echo # Build Manifest for RELEASE ${params.RELEASE} > ${MANIFEST}
                        echo # Last Updated: %DATE% %TIME% >> ${MANIFEST}
                        for %%F in (${RELEASE_DIR}\\*.jar) do echo %%~nxF >> ${MANIFEST}
                    """
                }
            }
        }

        stage('Archive Artifacts') {
            when { expression { params.BUILD_SERVICES || params.BUILD_SQL || params.BUILD_METADATA } }
            steps {
                echo "Archiving artifacts from ${RELEASE_DIR}"
                archiveArtifacts artifacts: "${RELEASE_DIR}/*", fingerprint: true
            }
        }
    }

    post {
        success {
            echo "✅ Pipeline completed successfully on branch: ${env.BRANCH_NAME}. Artifacts and manifest are in ${RELEASE_DIR}"
        }
        failure {
            echo "❌ Pipeline failed on branch: ${env.BRANCH_NAME}"
        }
    }
}