pipeline {
    agent any

    environment {
        SCANNER_HOME = tool 'SonarScanner'
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
                script {
                    try {
                        sh "${SCANNER_HOME}/bin/sonar-scanner -Dsonar.projectKey=TP-Jenkins"
                    } catch (Exception e) {
                        echo "SonarQube non configuré, on continue..."
                    }
                }
            }
        }

        stage('SCA Scan (Dependency-Check)') {
            steps {
                // On génère les rapports sans forcer l'échec ici
                dependencyCheck additionalArguments: '--scan requirements.txt --format ALL --enableExperimental', 
                                odcInstallation: 'DP-Check'
            }
        }
    }

    post {
        always {
            // ÉTAPE 11 : C'est ici qu'on bloque le build !
            // failedTotalHigh: 0 signifie : "Si le nombre de failles High (score 7-9) est > 0, échoue le build"
            // failedTotalCritical: 0 signifie : "Si le nombre de failles Critical (score 9-10) est > 0, échoue le build"
            dependencyCheckPublisher pattern: '**/dependency-check-report.xml', 
                                     failedTotalHigh: 0, 
                                     failedTotalCritical: 0
        }
    }
}
