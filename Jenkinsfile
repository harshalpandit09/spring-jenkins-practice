pipeline {
    agent any

    parameters {
        booleanParam(name: 'BUILD_SERVICES',  defaultValue: false, description: 'Build Services module')
        booleanParam(name: 'BUILD_SQL',       defaultValue: false, description: 'Build SQL module')
        booleanParam(name: 'BUILD_METADATA',  defaultValue: false, description: 'Build Metadata module')
        string(name: 'RELEASE', defaultValue: '25.2.0', description: 'Release version tag')
    }

    environment {
        BASE_DIR      = "D:\\MarketMapBuilds"
        DATE_TAG      = "${new Date().format('ddMM')}"
        BUILD_TAG     = "${params.RELEASE}.${DATE_TAG}.${env.BUILD_NUMBER}"
        RELEASE_DIR   = "${BASE_DIR}\\${params.RELEASE}"
        COMBINED_DIR  = "${RELEASE_DIR}\\CombinedBuild"
        MANIFEST_FILE = "${COMBINED_DIR}\\build_manifest.txt"
        EMAIL_RECIPIENTS = "harshalpandit09@gmail.com, sbmukhekar31@gmail.com"
    }

    stages {
        stage('Notify Build Start') {
            steps {
                script {
                    emailext(
                        to: "${EMAIL_RECIPIENTS}",
                        subject: "MarketMap Build STARTED - ${params.RELEASE}",
                        body: """
                            Hello Team,<br><br>
                            Jenkins build <b>${currentBuild.displayName}</b> for release <b>${params.RELEASE}</b> has <b>STARTED</b>.<br><br>
                            <b>Build Details:</b><br>
                            Build Number : ${env.BUILD_NUMBER}<br>
                            Release      : ${params.RELEASE}<br>
                            Branch       : ${env.BRANCH_NAME}<br><br>
                            You will receive another email once the build completes.<br><br>
                            Regards,<br>
                            Jenkins
                        """,
                        mimeType: 'text/html'
                    )
                }
            }
        }

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
                        move backend-webapi.${BUILD_TAG}.jar ${RELEASE_DIR}
                        del /Q ${COMBINED_DIR}\\backend-webapi.*.jar
                        copy /Y ${RELEASE_DIR}\\backend-webapi.${BUILD_TAG}.jar ${COMBINED_DIR}
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
                        move sql-service.${BUILD_TAG}.jar ${RELEASE_DIR}
                        del /Q ${COMBINED_DIR}\\sql-service.*.jar
                        copy /Y ${RELEASE_DIR}\\sql-service.${BUILD_TAG}.jar ${COMBINED_DIR}
                    """
                }
            }
        }

        stage('Build Metadata') {
            when { expression { params.BUILD_METADATA } }
            steps {
                script {
                    echo "Building Metadata module..."
                    // Uncomment to test failure:
                    // error("Forcing failure in Metadata step!")
                    bat "mvn clean package -f metadata-service/pom.xml -DskipTests"
                    bat """
                        cd metadata-service\\target
                        rename metadata-service-0.0.1-SNAPSHOT.jar metadata-service.${BUILD_TAG}.jar
                        move metadata-service.${BUILD_TAG}.jar ${RELEASE_DIR}
                        del /Q ${COMBINED_DIR}\\metadata-service.*.jar
                        copy /Y ${RELEASE_DIR}\\metadata-service.${BUILD_TAG}.jar ${COMBINED_DIR}
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
    }

    post {
        always {
            script {
                def duration = currentBuild.durationString.replace('and counting', '').trim()
                if (currentBuild.currentResult == 'SUCCESS') {
                    emailext(
                        to: "${EMAIL_RECIPIENTS}",
                        subject: "MarketMap Build SUCCESS - ${params.RELEASE}",
                        body: """
                            Hello Team,<br><br>
                            Jenkins build <b>${currentBuild.displayName}</b> for release <b>${params.RELEASE}</b> has <b>SUCCEEDED</b>.<br><br>
                            <b>Build Details:</b><br>
                            Build Number : ${env.BUILD_NUMBER}<br>
                            Release      : ${params.RELEASE}<br>
                            Branch       : ${env.BRANCH_NAME}<br>
                            Duration     : ${duration}<br><br>
                            Regards,<br>
                            Jenkins
                        """,
                        mimeType: 'text/html'
                    )
                } else {
                    def logFile = "${WORKSPACE}\\build_console_log.txt"
                    writeFile file: logFile, text: currentBuild.rawBuild.getLog(10000).join("\n")
                    emailext(
                        to: "${EMAIL_RECIPIENTS}",
                        subject: "MarketMap Build FAILED - ${params.RELEASE}",
                        body: """
                            Hello Team,<br><br>
                            Jenkins build <b>${currentBuild.displayName}</b> for release <b>${params.RELEASE}</b> has <b>FAILED</b>.<br><br>
                            <b>Build Details:</b><br>
                            Build Number : ${env.BUILD_NUMBER}<br>
                            Release      : ${params.RELEASE}<br>
                            Branch       : ${env.BRANCH_NAME}<br>
                            Duration     : ${duration}<br><br>
                            Please check the attached log for details.<br><br>
                            Regards,<br>
                            Jenkins
                        """,
                        attachmentsPattern: "build_console_log.txt",
                        mimeType: 'text/html'
                    )
                }
            }
        }
    }
}
