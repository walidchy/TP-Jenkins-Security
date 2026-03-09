pipeline {
    agent any

    environment {
        SCANNER_HOME = tool 'SonarScanner'
    }

    stages {
        stage('Clone Repository') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt --break-system-packages || pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                // Section 8 of TP: Runs the pytest file
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
                    -Dsonar.python.version=3
                    """
                }
            }
        }

        stage('SCA Scan (Dependency Check)') {
            steps {
                // Section 10 & 11 of TP: Generate report and check for vulnerabilities
                // odcInstallation must match the name in Manage Jenkins > Tools
                dependencyCheck additionalArguments: '--scan requirements.txt --format HTML --format XML',
                odcInstallation: 'DP-Check'
            }
        }
    }

    post {
        always {
            // This publishes the report in the Jenkins UI
            // Section 11: failedTotalHigh: 1 means if 1 High vuln is found, build FAILS
            dependencyCheckPublisher pattern: '**/dependency-check-report.xml',
                                     failedTotalHigh: 1, 
                                     failedTotalCritical: 1
        }
        failure {
            echo 'Build failed due to errors or security vulnerabilities'
        }
    }
}
