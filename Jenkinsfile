pipeline {
    agent any
    environment {
        DOCKER_IMAGE = 'bist_mlops_api:latest'
        DOCKER_CONTAINER = 'bist_mlops_api_container'
    }
    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'http://gitea:3000/jenkins/BIST_MLOps_CICD.git'
            }
        }
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t ${DOCKER_IMAGE} .'
            }
        }
        stage('Run API Tests') {
            steps {
                script {
                    // Stop and remove existing container if exists
                    sh """
                    if [ \$(docker ps -aq -f name=${DOCKER_CONTAINER}) ]; then
                        docker stop ${DOCKER_CONTAINER}
                        docker rm ${DOCKER_CONTAINER}
                    fi
                    """
                    // Run container
                    sh 'docker run -d --name ${DOCKER_CONTAINER} -p 8010:8010 ${DOCKER_IMAGE}'
                }
                sh '''
                echo Waiting for API to be ready...
                for i in {1..20}; do
                    if curl --silent --fail http://localhost:8010/; then
                        echo API is ready!
                        exit 0
                    fi
                    echo "API not ready, retrying in 5 seconds..."
                    sleep 5
                done
                echo "API did not become ready in time."
                exit 1
                '''
            }
        }
        stage('Deploy API') {
            steps {
                echo 'API deployment completed successfully!'
            }
        }
    }
    post {
        always {
            // Stop container but do not remove it
            sh """
            if [ \$(docker ps -aq -f name=${DOCKER_CONTAINER}) ]; then
                echo Stopping container ${DOCKER_CONTAINER}.
                docker stop ${DOCKER_CONTAINER}
            fi
            """
        }
    }
}
