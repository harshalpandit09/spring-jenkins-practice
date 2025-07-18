pipeline {
    agent any

    parameters {
        booleanParam(name: 'BUILD_SERVICES',  defaultValue: false, description: 'Build Services module')
        booleanParam(name: 'BUILD_SQL',       defaultValue: false, description: 'Build SQL module')
        booleanParam(name: 'BUILD_METADATA',  defaultValue: false, description: 'Build Metadata module')
        string(name: 'RELEASE', defaultValue: '25.2.0', description: 'Release version tag')
    }

    environment {
        DATE_TAG       = "${new Date().format('ddMM')}"
        BUILD_TAG      = "${params.RELEASE}.${new Date().format('ddMM')}.${env.BUILD_NUMBER}"
        RELEASE_DIR    = "Builds\\${params.RELEASE}"
        COMBINED_DIR   = "Builds\\${params.RELEASE}\\CombinedBuild"
        MANIFEST_FILE  = "Builds\\${params.RELEASE}\\CombinedBuild\\build_manifest.txt"
    }

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
                echo "Code checked out from branch: ${env.BRANCH_NAME}"
            }
        }

        stage('Prepare Folders') {
            when { expression { params.BUILD_SERVICES || params.BUILD_SQL || params.BUILD_METADATA } }
            steps {
                bat "if not exist ${RELEASE_DIR} mkdir ${RELEASE_DIR}"
                bat "if not exist ${COMBINED_DIR} mkdir ${COMBINED_DIR}"
            }
        }

        stage('Build Services') {
            when { expression { params.BUILD_SERVICES } }
            steps {
                script {
                    echo "Building Services module..."
                    bat "mvn clean package -f backend-webapi/pom.xml -DskipTests"
                    bat """
                        cd backend-webapi\\target
                        rename backend-webapi-0.0.1-SNAPSHOT.jar backend-webapi.${BUILD_TAG}.jar
                        move backend-webapi.${BUILD_TAG}.jar ..\\..\\${RELEASE_DIR}
                        del /Q ..\\..\\${COMBINED_DIR}\\backend-webapi.*.jar
                        copy /Y ..\\..\\${RELEASE_DIR}\\backend-webapi.${BUILD_TAG}.jar ..\\..\\${COMBINED_DIR}\\backend-webapi.${BUILD_TAG}.jar
                    """
                }
            }
        }

        stage('Build SQL') {
            when { expression { params.BUILD_SQL } }
            steps {
                script {
                    echo "Building SQL module..."
                    bat "mvn clean package -f sql-service/pom.xml -DskipTests"
                    bat """
                        cd sql-service\\target
                        rename sql-service-0.0.1-SNAPSHOT.jar sql-service.${BUILD_TAG}.jar
                        move sql-service.${BUILD_TAG}.jar ..\\..\\${RELEASE_DIR}
                        del /Q ..\\..\\${COMBINED_DIR}\\sql-service.*.jar
                        copy /Y ..\\..\\${RELEASE_DIR}\\sql-service.${BUILD_TAG}.jar ..\\..\\${COMBINED_DIR}\\sql-service.${BUILD_TAG}.jar
                    """
                }
            }
        }

        stage('Build Metadata') {
            when { expression { params.BUILD_METADATA } }
            steps {
                script {
                    echo "Building Metadata module..."
                    bat "mvn clean package -f metadata-service/pom.xml -DskipTests"
                    bat """
                        cd metadata-service\\target
                        rename metadata-service-0.0.1-SNAPSHOT.jar metadata-service.${BUILD_TAG}.jar
                        move metadata-service.${BUILD_TAG}.jar ..\\..\\${RELEASE_DIR}
                        del /Q ..\\..\\${COMBINED_DIR}\\metadata-service.*.jar
                        copy /Y ..\\..\\${RELEASE_DIR}\\metadata-service.${BUILD_TAG}.jar ..\\..\\${COMBINED_DIR}\\metadata-service.${BUILD_TAG}.jar
                    """
                }
            }
        }

        stage('Update Combined Manifest') {
            when { expression { params.BUILD_SERVICES || params.BUILD_SQL || params.BUILD_METADATA } }
            steps {
                echo "Rebuilding manifest file in ${MANIFEST_FILE}"
                bat "del /Q ${MANIFEST_FILE} || echo No old manifest"
                bat """
                    echo # Build Manifest for RELEASE ${params.RELEASE} > ${MANIFEST_FILE}
                    echo # Last Updated: %DATE% %TIME% >> ${MANIFEST_FILE}
                    for %%F in (${COMBINED_DIR}\\*.jar) do echo %%~nxF >> ${MANIFEST_FILE}
                """
            }
        }

        stage('Summary of Combined Build') {
            when { expression { params.BUILD_SERVICES || params.BUILD_SQL || params.BUILD_METADATA } }
            steps {
                echo "##### Summary of Combined Build #####"
                bat "type ${MANIFEST_FILE}"
            }
        }

        stage('Archive Artifacts') {
            when { expression { params.BUILD_SERVICES || params.BUILD_SQL || params.BUILD_METADATA } }
            steps {
                echo "Archiving artifacts from ${RELEASE_DIR} and ${COMBINED_DIR}"
                archiveArtifacts artifacts: "${RELEASE_DIR}/*, ${COMBINED_DIR}/*", fingerprint: true
            }
        }
    }

    post {
        success {
            echo "✅ Pipeline completed successfully. Latest combined builds are in ${COMBINED_DIR}"
        }
        failure {
            echo "❌ Pipeline failed on branch: ${env.BRANCH_NAME}"
        }
    }
}