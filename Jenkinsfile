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
                bat 'docker-compose down -v --remove-orphans'
                bat 'docker-compose up -d'
            }
        }
    }

    post {
        failure {
            echo 'Pipeline gagal! Deploy dibatalkan.'
            emailext(
                subject: "❌ Jenkins Build GAGAL - ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
                    <h2>Pipeline Gagal!</h2>
                    <p><b>Project:</b> ${env.JOB_NAME}</p>
                    <p><b>Build:</b> #${env.BUILD_NUMBER}</p>
                    <p><b>Status:</b> FAILURE</p>
                    <p><b>Detail:</b> <a href="${env.BUILD_URL}">Klik di sini</a></p>
                """,
                to: 'cycwag3006@gmail.com',
                mimeType: 'text/html'
            )
        }
        success {
            echo 'Semua test lulus! App berhasil di-deploy.'
            emailext(
                subject: "✅ Jenkins Build SUKSES - ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
                    <h2>Pipeline Berhasil!</h2>
                    <p><b>Project:</b> ${env.JOB_NAME}</p>
                    <p><b>Build:</b> #${env.BUILD_NUMBER}</p>
                    <p><b>Status:</b> SUCCESS</p>
                    <p><b>Detail:</b> <a href="${env.BUILD_URL}">Klik di sini</a></p>
                """,
                to: 'cycwag3006@gmail.com',
                mimeType: 'text/html'
            )
        }
    }
}