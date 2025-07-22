pipeline {
    agent any

    parameters {
        choice(name: 'COMPONENTS', choices: ['Services', 'SQL', 'Metadata', 'All'], description: 'Select components to build')
        string(name: 'RELEASE_VERSION', defaultValue: '25.2.0', description: 'Release Version')
        booleanParam(name: 'PUSH_TO_ECR', defaultValue: true, description: 'Push Docker Images to AWS ECR')
        booleanParam(name: 'UPLOAD_JARS', defaultValue: false, description: 'Upload JARs to S3')
    }

    environment {
        BUILD_DIR = "D:\\MarketMapBuilds\\${params.RELEASE_VERSION}\\CombinedBuild"
        AWS_ACCOUNT_ID = "969258966375"
        REGION = "eu-north-1"
    }

    stages {
        stage('Show Selections') {
            steps {
                script {
                    echo "========= Pipeline Configuration ========="
                    echo "Components     : ${params.COMPONENTS}"
                    echo "Release Version: ${params.RELEASE_VERSION}"
                    echo "Push to ECR    : ${params.PUSH_TO_ECR}"
                    echo "Upload JARs    : ${params.UPLOAD_JARS}"
                    echo "=========================================="
                }
            }
        }

        stage('Build & Push Docker Images') {
            steps {
                script {
                    def comps = []
                    if (params.COMPONENTS == "All") {
                        comps = ['backend-webapi', 'sql-service', 'metadata-service']
                    } else if (params.COMPONENTS == "Services") {
                        comps = ['backend-webapi']
                    } else if (params.COMPONENTS == "SQL") {
                        comps = ['sql-service']
                    } else if (params.COMPONENTS == "Metadata") {
                        comps = ['metadata-service']
                    }

                    withAWS(region: "${REGION}", credentials: 'aws-jenkins') {
                        bat """
                        aws ecr get-login-password --region ${REGION} | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com
                        """

                        comps.each { comp ->
                            bat """
                            python build_push_backend.py ${comp} ${params.RELEASE_VERSION} ${params.PUSH_TO_ECR}
                            """
                        }
                    }
                }
            }
        }

        stage('Upload JARs to S3') {
            when { expression { params.UPLOAD_JARS } }
            steps {
                withAWS(region: "${REGION}", credentials: 'aws-jenkins') {
                    bat """
                    aws s3 sync "${BUILD_DIR}" s3://marketmap-builds/${params.RELEASE_VERSION}/
                    """
                }
            }
        }

        stage('Summary') {
            steps {
                echo "Pipeline completed successfully!"
            }
        }
    }

    post {
        failure {
            echo "❌ Pipeline failed."
        }
    }
}
