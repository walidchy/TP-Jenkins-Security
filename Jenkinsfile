pipeline {
    agent any

    environment {
        SCANNER_HOME = tool 'SonarScanner'
        SONAR_TOKEN = credentials('sonarqube-token')
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt --break-system-packages'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'python3 -m pytest test_app.py'
            }
        }

        stage('SAST Scan (SonarQube)') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    sh """
                    ${SCANNER_HOME}/bin/sonar-scanner \
                    -Dsonar.projectKey=TP-Jenkins \
                    -Dsonar.sources=. \
                    -Dsonar.host.url=http://host.docker.internal:9000 \
                    -Dsonar.login=${SONAR_TOKEN}
                    """
                }
            }
        }

        stage('SCA Scan (Dependency Check)') {
            steps {
                dependencyCheck additionalArguments: '--scan requirements.txt --format ALL --enableExperimental',
                odcInstallation: 'DP-Check'
            }
        }
    }

    post {
        always {
            dependencyCheckPublisher pattern: '**/dependency-check-report.xml',
            failedTotalHigh: 0,
            failedTotalCritical: 0
        }
    }
}
