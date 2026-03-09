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

        stage('SAST Scan (SonarQube)') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    sh "${SCANNER_HOME}/bin/sonar-scanner -Dsonar.projectKey=TP-Jenkins -Dsonar.sources=."
                }
            }
        }

        stage('SCA Scan (Dependency-Check)') {
            steps {
                // 1. Lance l'analyse de sécurité
                dependencyCheck additionalArguments: '--scan requirements.txt --format XML --enableExperimental',
                odcInstallation: 'DP-Check'
                
                // 2. Affiche les résultats automatiquement dans la console
                script {
                    echo "--- SECURITY ALERT: VULNERABLE LIBRARIES DETECTED ---"
                    sh '''
                    grep -B 10 "vulnerability" dependency-check-report.xml | grep "fileName" | sed 's/<[^>]*>//g' | sort -u
                    '''
                    echo "------------------------------------------------------"
                }
            }
        }
    }

    post {
        always {
            // Met le build en ROUGE s'il y a une faille High ou Critical (Seuil à 0)
            dependencyCheckPublisher pattern: '**/dependency-check-report.xml',
                                     failedTotalHigh: 0, 
                                     failedTotalCritical: 0
        }
        failure {
            echo "BUILD STOPPED: Security vulnerabilities found in requirements.txt"
        }
    }
}
