pipeline {
    agent any

    parameters {
        booleanParam(name: 'BUILD_SERVICES',  defaultValue: false, description: 'Build Services module')
        booleanParam(name: 'BUILD_SQL',       defaultValue: false, description: 'Build SQL module')
        booleanParam(name: 'BUILD_METADATA',  defaultValue: false, description: 'Build Metadata module')
        string(name: 'RELEASE', defaultValue: '24.7.0', description: 'Release version tag')
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
                script {
                    checkout scm
                    echo "Code checked out from branch: ${env.BRANCH_NAME}"
                }
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
                    // Uncomment below line only for testing failure
                    //error("Forcing failure in Metadata step!")
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
                script {
                    echo "Rebuilding manifest file in ${MANIFEST_FILE}"
                    bat "del /Q ${MANIFEST_FILE} || echo No old manifest"
                    bat """
                        echo # Build Manifest for RELEASE ${params.RELEASE} > ${MANIFEST_FILE}
                        echo # Last Updated: %DATE% %TIME% >> ${MANIFEST_FILE}
                        for %%F in (${COMBINED_DIR}\\*.jar) do echo %%~nxF >> ${MANIFEST_FILE}
                    """
                }
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
        success {
            emailext(
                to: "${EMAIL_RECIPIENTS}",
                subject: "MarketMap Build SUCCESS - ${params.RELEASE}",
                body: """
                    Hello Team,<br><br>
                    Build <b>${currentBuild.displayName}</b> completed <b>SUCCESSFULLY</b>.<br>
                    <b>Build Number:</b> ${env.BUILD_NUMBER}<br>
                    <b>Branch:</b> ${env.BRANCH_NAME}<br>
                    <b>Release:</b> ${params.RELEASE}<br>
                    <b>Start Time:</b> ${currentBuild.startTimeInMillis}<br>
                    <b>Duration:</b> ${currentBuild.durationString}<br><br>
                    Regards,<br>
                    Jenkins
                """,
                mimeType: 'text/html',
                attachLog: false
            )
        }

        failure {
            emailext(
                to: "${EMAIL_RECIPIENTS}",
                subject: "MarketMap Build FAILED - ${params.RELEASE}",
                body: """
                    Hello Team,<br><br>
                    Build <b>${currentBuild.displayName}</b> has <b>FAILED</b>.<br>
                    <b>Build Number:</b> ${env.BUILD_NUMBER}<br>
                    <b>Branch:</b> ${env.BRANCH_NAME}<br>
                    <b>Release:</b> ${params.RELEASE}<br>
                    <b>Start Time:</b> ${currentBuild.startTimeInMillis}<br>
                    Duration: ${currentBuild.durationString}<br><br>
                    Please check the attached log.<br>
                    Regards,<br>
                    Jenkins
                """,
                mimeType: 'text/html',
                attachLog: true
            )
        }
    }
}
