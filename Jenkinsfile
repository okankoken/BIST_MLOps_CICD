pipeline {
    agent any
    environment {
        GITEA_TOKEN = '191a7cafbd975f568ba18bea6bcf218d1af8c578'
    }
    stages {
        stage('Clone Repository') {
            steps {
                script {
                    checkout([
                        $class: 'GitSCM',
                        branches: [[name: '*/main']],
                        userRemoteConfigs: [[
                            url: 'http://gitea:3000/jenkins/BIST_MLOps_CICD.git',
                            credentialsId: 'gitea-credentials',
                            refspec: '+refs/heads/*:refs/remotes/origin/*',
                            // HTTP Header ile Token ekleme
                            httpHeaders: [[name: 'Authorization', value: 'token ${env.GITEA_TOKEN}']]
                        ]]
                    ])
                }
            }
        }
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t bist_mlops_api:latest .'
            }
        }
        stage('Run API Tests') {
            steps {
                script {
                    sh """
                    if [ \$(docker ps -aq -f name=bist_mlops_api_container) ]; then
                        docker stop bist_mlops_api_container || true
                        docker rm bist_mlops_api_container || true
                    fi
                    """
                    sh 'docker run -d --name bist_mlops_api_container -p 8010:8010 bist_mlops_api:latest'
                    sh 'sleep 5'
                    sh 'curl --silent --fail http://localhost:8010/'
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
            echo "Pipeline tamamlandi. API erisilebilir durumda."
        }
    }
}
