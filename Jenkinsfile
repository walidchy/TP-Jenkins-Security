pipeline {
    agent any

    environment {
        // Nom de l'outil configuré dans Administrer Jenkins > Tools
        SCANNER_HOME = tool 'SonarScanner'
    }

    stages {
        stage('Clone Repository') {
            steps {
                // SOLUTION : Utiliser 'checkout scm' au lieu de la commande git manuelle.
                // Cela utilise automatiquement la branche 'main' et les réglages du projet.
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                // Installation des bibliothèques listées dans requirements.txt
                sh 'pip install -r requirements.txt --break-system-packages'
            }
        }

        stage('Run Tests') {
            steps {
                // Exécution des tests unitaires (Étape 8 du TP)
                sh 'python3 -m pytest test_app.py'
            }
        }

        stage('SAST Scan (SonarQube)') {
            steps {
                script {
                    try {
                        // Analyse du code source (Étape 9 du TP)
                        sh "${SCANNER_HOME}/bin/sonar-scanner -Dsonar.projectKey=TP-Jenkins"
                    } catch (Exception e) {
                        echo "SonarQube non configuré ou injoignable, on continue le TP..."
                    }
                }
            }
        }

        stage('SCA Scan (Dependency-Check)') {
            steps {
                // Analyse des dépendances et BLOCAGE si score > 7 (Étape 10 & 11 du TP)
                // L'installation doit s'appeler 'DP-Check' dans vos outils Jenkins.
                dependencyCheck additionalArguments: '--scan . --format HTML --format XML --failBuildOnCVSS 7', odcInstallation: 'DP-Check'
            }
        }
    }

    post {
        always {
            // Publie le rapport XML pour que Jenkins puisse l'analyser
            dependencyCheckPublisher pattern: '**/dependency-check-report.xml'
        }
        failure {
            echo 'Le build a échoué ! Raison possible : Test échoué OU Vulnérabilité critique trouvée (CVSS > 7).'
        }
    }
}
