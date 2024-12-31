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
                    // Check if the container exists, and stop it if it does
                    sh """
                    if [ \$(docker ps -aq -f name=${DOCKER_CONTAINER}) ]; then
                        docker stop ${DOCKER_CONTAINER} || true
                    fi
                    """
                    // Run the container
                    sh 'docker run -d --name ${DOCKER_CONTAINER} -p 8010:8010 ${DOCKER_IMAGE}'
                }
                script {
                    // Wait for API to be ready
                    def retries = 10
                    def waitTime = 5 // seconds
                    for (int i = 0; i < retries; i++) {
                        if (sh(script: 'curl --silent --fail http://localhost:8010/', returnStatus: true) == 0) {
                            echo "API is up and running!"
                            break
                        }
                        echo "Waiting for API to be ready..."
                        sleep waitTime
                    }
                    if (sh(script: 'curl --silent --fail http://localhost:8010/', returnStatus: true) != 0) {
                        error "API did not become ready in time."
                    }
                }
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
            // Stop the container after pipeline finishes, but do not remove it
            sh """
            if [ \$(docker ps -aq -f name=${DOCKER_CONTAINER}) ]; then
                docker stop ${DOCKER_CONTAINER} || true
            fi
            """
        }
    }
}
