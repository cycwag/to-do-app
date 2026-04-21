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
                bat 'docker-compose run --rm --no-deps web pytest test_app.py -v'
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying app...'
                bat 'docker-compose down'
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