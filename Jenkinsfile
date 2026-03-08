pipeline {
    agent any

    environment {
        // Nom de l'outil configuré dans Jenkins > Tools
        SCANNER_HOME = tool 'SonarScanner'
    }

    stages {
        stage('Checkout') {
            steps {
                // Utilise la configuration automatique de Jenkins
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                // Installation des bibliothèques (Flask, Requests, etc.)
                sh 'pip install -r requirements.txt --break-system-packages'
            }
        }

        stage('Run Tests') {
            steps {
                // Étape 8 du TP : Exécution des tests unitaires
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
                // On force le scan sur le fichier requirements.txt spécifiquement
                dependencyCheck additionalArguments: '''
                    --scan requirements.txt 
                    --format HTML 
                    --format XML 
                    --failOnCVSS 7 
                    --enableExperimental
                ''', odcInstallation: 'DP-Check'
            }
        }
    }

    post {
        always {
            // Affiche le rapport de sécurité dans l'interface Jenkins
            dependencyCheckPublisher pattern: '**/dependency-check-report.xml'
        }
        failure {
            echo 'Le build a échoué ! Cause possible : Test échoué OU Vulnérabilité critique (CVSS > 7).'
        }
    }
} 
