pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo 'Building Docker image...'
                bat 'docker-compose build'
            }
        }
        stage('Test') {
            steps {
                echo 'Running tests...'
                bat 'docker-compose run --rm web pytest test_app.py -v'
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying app...'
                bat 'docker-compose down'
                bat 'docker ps -q --filter "publish=5000" | findstr . && docker stop $(docker ps -q --filter "publish=5000") || echo no container on 5000'
                bat 'docker-compose up -d'
            }
        }
    }

    post {
        failure {
            echo 'Pipeline gagal! Deploy dibatalkan.'
        }
        success {
            echo 'Semua test lulus! App berhasil di-deploy.'
        }
    }
}