pipeline {
    agent any
    environment {
        API_CONTAINER_NAME = "bist_mlops_api_container"
        API_PORT = "8010"
    }
    stages {
        stage('Clone Repository') {
            steps {
                git credentialsId: 'gitea-username-password', url: 'http://gitea:3000/jenkins/BIST_MLOps_CICD.git'
            }
        }
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t bist_mlops_api:latest .'
            }
        }
        stage('Run API Tests') {
            steps {
                // Daha önceki container varsa durdurup sil
                sh """
                docker ps -aq -f name=${API_CONTAINER_NAME} | xargs -r docker stop
                docker ps -aq -f name=${API_CONTAINER_NAME} | xargs -r docker rm
                """
                // Yeni container baslat
                sh "docker run -d --name ${API_CONTAINER_NAME} -p ${API_PORT}:${API_PORT} bist_mlops_api:latest"
                // Uygulamanin tamamen baslatilmasi için bekle
                sh 'sleep 15'
                // Container içini kontrol et
                sh 'docker ps'
                sh 'docker logs ${API_CONTAINER_NAME}'
                // Ag durumunu kontrol et
                sh 'docker network inspect mlops-net'
                sh "docker exec jenkins ping -c 3 ${API_CONTAINER_NAME}"
                // API'yi test et
                sh "curl -v http://localhost:${API_PORT}/"
            }
        }
    }
    post {
        always {
            echo 'Pipeline tamamlandi.'
        }
        failure {
            echo 'Pipeline basarisiz oldu.'
        }
    }
}
