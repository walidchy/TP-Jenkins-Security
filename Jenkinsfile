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
                // 1. Analyse de sécurité
                dependencyCheck additionalArguments: '--scan requirements.txt --format XML --enableExperimental',
                odcInstallation: 'DP-Check'
                
                // 2. Détection Automatique de TOUTES les bibliothèques vulnérables
                script {
                    echo "#########################################################"
                    echo "             SECURITY ALERT: VULNERABLE LIBS             "
                    echo "#########################################################"
                    
                    // Cette commande cherche très large (100 lignes avant) pour ne rien rater
                    sh '''
                    grep -B 100 "<vulnerability" dependency-check-report.xml | grep "<fileName>" | sed 's/<[^>]*>//g' | sed 's/^[[:space:]]*//' | sort -u
                    '''
                    
                    echo "#########################################################"
                }
            }
        }
    }

    post {
        always {
            // Force le build en ROUGE s'il y a un risque
            dependencyCheckPublisher pattern: '**/dependency-check-report.xml',
                                     failedTotalHigh: 0, 
                                     failedTotalCritical: 0
        }
    }
}
