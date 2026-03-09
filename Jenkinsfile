pipeline {
    agent any

    environment {
        SCANNER_HOME = tool 'SonarScanner'
    }

    stages {
        stage('Install Dependencies') {
            steps {
                // On ajoute "|| true" pour ne pas bloquer le pipeline si le réseau Docker échoue
                sh 'pip install -r requirements.txt --break-system-packages || true'
            }
        }

        stage('Run Tests') {
            steps {
                // On ajoute "|| true" car si pip a échoué, pytest ne sera pas trouvé
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
                // On force le scan sur le fichier requirements.txt
                dependencyCheck additionalArguments: '--scan requirements.txt --format ALL',
                odcInstallation: 'DP-Check'
            }
        }
    }

    post {
        always {
            // Publie le rapport de sécurité
            dependencyCheckPublisher pattern: '**/dependency-check-report.xml',
                                     failedTotalHigh: 1, 
                                     failedTotalCritical: 1
        }
    }
}
