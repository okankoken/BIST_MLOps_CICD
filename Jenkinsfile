pipeline {
    agent any
    stages {
        stage('Clone Repository') {
            steps {
                git 'https://github.com/okankoken/BIST_MLops.git'
            }
        }
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t bist-mlops-api .'
            }
        }
        stage('Run API Tests') {
            steps {
                sh 'docker run --rm bist-mlops-api python scripts/model_training.py'
            }
        }
        stage('Deploy API') {
            steps {
                sh 'docker run -d -p 8000:8000 --name bist-mlops bist-mlops-api'
            }
        }
    }
}
