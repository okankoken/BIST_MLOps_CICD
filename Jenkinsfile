pipeline {
    agent any
    environment {
        API_CONTAINER_NAME = "bist_mlops_api_container"
        API_PORT = "8010"
    }
    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', // Varsayilan branch ayari. Gerekiyorsa master olarak degistirin.
                    credentialsId: 'gitea-username-password', 
                    url: 'http://gitea:3000/jenkins/BIST_MLOps_CICD.git'
            }
        }
        stage('Build Docker Image') {
            steps {
                echo 'Docker image olusturuluyor...'
                sh 'docker build -t bist_mlops_api:latest .'
            }
        }
        stage('Run API Tests') {
            steps {
                script {
                    echo 'Önceki container kontrol ediliyor ve durduruluyor...'
                    sh """
                    docker ps -aq -f name=${API_CONTAINER_NAME} | xargs -r docker stop
                    docker ps -aq -f name=${API_CONTAINER_NAME} | xargs -r docker rm
                    """
                    echo 'Yeni container baslatiliyor...'
                    sh "docker run -d --name ${API_CONTAINER_NAME} -p ${API_PORT}:${API_PORT} bist_mlops_api:latest"
                    echo 'Containerin tamamen baslatilmasi için bekleniyor...'
                    sh 'sleep 15'

                    echo 'Container kontrol ediliyor...'
                    sh 'docker ps'
                    sh 'docker logs ${API_CONTAINER_NAME}'

                    echo 'Ag baglantisi kontrol ediliyor...'
                    sh 'docker network inspect mlops-net'
                    sh "docker exec jenkins ping -c 3 ${API_CONTAINER_NAME}"

                    echo 'API test ediliyor...'
                    sh "curl -v http://localhost:${API_PORT}/"
                }
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
