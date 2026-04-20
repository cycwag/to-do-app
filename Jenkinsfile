pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo 'Building Docker image...'
                bat 'docker-compose build'
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying app...'
                bat 'docker-compose up -d'
            }
        }
    }
}