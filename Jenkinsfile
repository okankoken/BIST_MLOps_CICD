pipeline {
    agent any

    stages {
        stage('Clone Repository') {
            steps {
                // Gitea repository'sini klonlamak için doğru URL ve credentials
                git url: 'http://localhost:3000/jenkins/BIST_MLOps_CICD.git', 
                    branch: 'main', 
                    credentialsId: 'gitea-credentials'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker Image...'
                sh 'docker build -t bist-mlops-api .'
            }
        }

        stage('Run API Tests') {
            steps {
                echo 'Running API Tests...'
                sh 'python -m unittest discover tests'
            }
        }

        stage('Deploy API') {
            steps {
                echo 'Deploying API...'
                sh 'docker run -d -p 8000:8000 bist-mlops-api'
            }
        }
    }

    post {
        always {
            echo 'Pipeline execution completed.'
        }
        success {
            echo 'Pipeline completed successfully.'
        }
        failure {
            echo 'Pipeline failed. Check the logs.'
        }
    }
}
