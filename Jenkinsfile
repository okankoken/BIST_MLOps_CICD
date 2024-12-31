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
                    // Check if the container exists, stop and remove if needed
                    sh """
                    if [ \$(docker ps -aq -f name=${DOCKER_CONTAINER}) ]; then
                        echo "Container ${DOCKER_CONTAINER} already exists."
                        docker stop ${DOCKER_CONTAINER} || true
                        docker rm ${DOCKER_CONTAINER} || true
                    fi
                    """
                    // Run a new container
                    sh 'docker run -d --name ${DOCKER_CONTAINER} -p 8010:8010 ${DOCKER_IMAGE}'
                }
                // Wait for the container to start and API to be ready
                sh """
                for i in {1..10}; do
                    if curl --silent --fail http://localhost:8010/; then
                        echo "API is ready."
                        exit 0
                    fi
                    echo "Waiting for API to be ready..."
                    sleep 5
                done
                echo "API did not become ready in time."
                exit 1
                """
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
            // Stop the container after pipeline finishes
            sh """
            if [ \$(docker ps -aq -f name=${DOCKER_CONTAINER}) ]; then
                echo "Stopping container ${DOCKER_CONTAINER}."
                docker stop ${DOCKER_CONTAINER} || true
            fi
            """
        }
    }
}
