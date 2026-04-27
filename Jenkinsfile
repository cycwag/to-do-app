pipeline {
    agent any

    environment {
        EC2_IP = '16.79.142.118'
        EC2_USER = 'ubuntu'
    }

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
        stage('Deploy to EC2') {
            steps {
                echo 'Deploying to EC2...'
              bat """
                        ssh -i "C:\\Program Files\\Jenkins\\to-do-app.pem" -o StrictHostKeyChecking=no ubuntu@16.79.142.118 "cd /home/ubuntu/to-do-app && git pull origin main && docker compose down -v && docker compose up -d --build"
                    """
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
                    <p><b>Detail:</b> <a href="${env.BUILD_URL}">Klik di sini</a></p>
                """,
                to: 'cycwag3006@gmail.com',
                mimeType: 'text/html'
            )
        }
        success {
            echo 'Semua test lulus! App berhasil di-deploy ke EC2.'
            emailext(
                subject: "✅ Jenkins Build SUKSES - ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
                    <h2>Pipeline Berhasil!</h2>
                    <p><b>Project:</b> ${env.JOB_NAME}</p>
                    <p><b>Build:</b> #${env.BUILD_NUMBER}</p>
                    <p><b>Detail:</b> <a href="${env.BUILD_URL}">Klik di sini</a></p>
                """,
                to: 'cycwag3006@gmail.com',
                mimeType: 'text/html'
            )
        }
    }
}