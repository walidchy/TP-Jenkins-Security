pipeline {
    agent any

    environment {
        SCANNER_HOME = tool 'SonarScanner'
    }

    stages {
        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt --break-system-packages'
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
                // 1. Lance l'analyse
                dependencyCheck additionalArguments: '--scan requirements.txt --format XML --enableExperimental',
                odcInstallation: 'DP-Check'
                
                // 2. Détection Automatique Propre
                script {
                    echo "--- VULNERABILITY ALERT ---"
                    sh '''
                    awk -v RS='<dependency' '/<vulnerability/ {match($0, /<fileName>[^<]+/); print "[!] VULNERABLE: " substr($0, RSTART+10, RLENGTH-10)}' dependency-check-report.xml | sort -u
                    '''
                    echo "---------------------------"
                }
            }
        }
    }

    post {
        always {
            // Force le build en ROUGE
            dependencyCheckPublisher pattern: '**/dependency-check-report.xml',
                                     failedTotalHigh: 0, 
                                     failedTotalCritical: 0
        }
        failure {
            echo "STOP: Critical vulnerabilities detected. Check the list above."
        }
    }
}
