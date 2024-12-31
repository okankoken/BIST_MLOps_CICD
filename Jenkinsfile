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
                    // Check if the container exists, and stop/remove it if it does
                    sh """
                    if [ \$(docker ps -aq -f name=${DOCKER_CONTAINER}) ]; then
                        docker stop ${DOCKER_CONTAINER} || true
                        docker rm ${DOCKER_CONTAINER} || true
                    fi
                    """
                    // Run the container
                    sh 'docker run -d --name ${DOCKER_CONTAINER} -p 8010:8010 ${DOCKER_IMAGE}'
                }
                sh 'sleep 5' // Ensure container is up
                sh 'curl http://localhost:8010/' // Test if API is running
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
            // Stop and remove the container after pipeline finishes
            sh """
            if [ \$(docker ps -aq -f name=${DOCKER_CONTAINER}) ]; then
                docker stop ${DOCKER_CONTAINER} || true
                docker rm ${DOCKER_CONTAINER} || true
            fi
            """
        }
    }
}
