pipeline {
    agent any

    environment {
        SCANNER_HOME = tool 'SonarScanner'
    }

    stages {
        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt --break-system-packages || true'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'python3 -m pytest test_app.py || true'
            }
        }

        stage('SAST Scan (SonarQube)') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    sh "${SCANNER_HOME}/bin/sonar-scanner -Dsonar.projectKey=TP-Jenkins -Dsonar.sources=."
                }
            }
        }

        stage('SCA Scan (Dependency-Check)') {
            steps {
                // Added --enableExperimental to make sure it catches everything in requirements.txt
                dependencyCheck additionalArguments: '--scan requirements.txt --format ALL --enableExperimental',
                odcInstallation: 'DP-Check'
            }
        }
    }

    post {
        always {
            // CHANGE: Set thresholds to 0 to force RED on any finding
            dependencyCheckPublisher pattern: '**/dependency-check-report.xml',
                                     failedTotalHigh: 0, 
                                     failedTotalCritical: 0,
                                     failedTotalMedium: 0
        }
    }
}
