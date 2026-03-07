pipeline {
    agent any

    stages {

        stage('Clone Repository') {
            steps {
                git 'https://github.com/walidchy/TP-Jenkins-Security.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'pytest'
            }
        }

        stage('SCA Scan') {
            steps {
                sh 'dependency-check.sh --project "TP-Jenkins" --scan . --format HTML'
            }
        }
    }

    post {
        failure {
            echo 'Build failed due to errors or vulnerabilities'
        }
    }
}