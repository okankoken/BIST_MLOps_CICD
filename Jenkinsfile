pipeline {
    agent any
    environment {
        API_CONTAINER_NAME = "bist_mlops_api_container"
        API_PORT = "8010"
        NETWORK_NAME = "02_mlops_docker_mlops-net"
        MYSQL_CONTAINER_NAME = "mysql"
        MYSQL_HOST = "172.18.0.3"
        MYSQL_PORT = "3306"
        MLFLOW_CONTAINER_NAME = "mlflow_server"
        MLFLOW_HOST = "172.18.0.4"
        MLFLOW_PORT = "5000"
    }
    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main',
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
        stage('Run MySQL and MLflow Checks') {
            steps {
                script {
                    echo 'MySQL ve MLflow containerlari kontrol ediliyor...'
                    
                    // MySQL kontrolü
                    sh """
                    docker inspect -f '{{.State.Running}}' ${MYSQL_CONTAINER_NAME} || 
                    echo "MySQL container calismiyor!"
                    """
                    sh "nc -zv ${MYSQL_HOST} ${MYSQL_PORT}"

                    // MLflow kontrolü
                    sh """
                    docker inspect -f '{{.State.Running}}' ${MLFLOW_CONTAINER_NAME} || 
                    echo "MLflow container calismiyor!"
                    """
                    sh "curl -v http://${MLFLOW_HOST}:${MLFLOW_PORT}/"
                }
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
                    sh "docker run -d --name ${API_CONTAINER_NAME} --network ${NETWORK_NAME} -p ${API_PORT}:${API_PORT} bist_mlops_api:latest"
                    
                    echo 'Containerin tamamen baslatilmasi için bekleniyor...'
                    sh 'sleep 30'

                    echo 'API test ediliyor...'
                    sh "curl -v http://${API_CONTAINER_NAME}:${API_PORT}/"
                    sh "curl -v http://${API_CONTAINER_NAME}:${API_PORT}/predict?stock_name=AGROT.IS"
                }
            }
        }
        stage('Verify MySQL Entries') {
            steps {
                script {
                    echo 'MySQL tahmin kayitlari kontrol ediliyor...'
                    sh """
                    docker exec ${MYSQL_CONTAINER_NAME} mysql -u root -pAnkara06 -e "USE mlops_db; SELECT * FROM bist_predictions;"
                    """
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
