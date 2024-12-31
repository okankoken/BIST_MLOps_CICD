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
                    // Var olan konteyneri durdur ve kaldir
                    sh """
                    if [ \$(docker ps -aq -f name=${DOCKER_CONTAINER}) ]; then
                        echo "Stopping and removing existing container..."
                        docker stop ${DOCKER_CONTAINER} || true
                        docker rm ${DOCKER_CONTAINER} || true
                    fi
                    """
                    // Yeni konteyneri baslat
                    sh 'docker run -d --name ${DOCKER_CONTAINER} -p 8010:8010 ${DOCKER_IMAGE}'
                }
                // API'nin hazir olup olmadigini kontrol et
                sh """
                echo "Waiting for API to be ready..."
                for i in {1..20}; do
                    if curl --silent --fail http://localhost:8010/; then
                        echo "API is ready!"
                        exit 0
                    fi
                    echo "API not ready yet. Retrying in 5 seconds..."
                    sleep 5
                done
                echo "API did not become ready in time. Exiting..."
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
            echo "Pipeline tamamlandi. API çalismaya devam ediyor ve erisilebilir durumda."
        }
    }
}
