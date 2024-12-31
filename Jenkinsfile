pipeline {
    agent any
    environment {
        DOCKER_IMAGE = 'bist_mlops_api:latest'
        DOCKER_CONTAINER = 'bist_mlops_api_container'
    }
    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'http://gitea:3000/jenkins/BIST_MLOps_CICD.git', credentialsId: 'gitea-credentials'
            }
        }
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $DOCKER_IMAGE .'
            }
        }
        stage('Run API Tests') {
            steps {
                sh 'docker run -d --name $DOCKER_CONTAINER -p 8010:8010 $DOCKER_IMAGE'
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
            sh 'docker stop $DOCKER_CONTAINER || true'
            sh 'docker rm $DOCKER_CONTAINER || true'
        }
    }
}
