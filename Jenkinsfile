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
                // 1. Generate only the XML format to keep it clean
                dependencyCheck additionalArguments: '--scan requirements.txt --format XML --enableExperimental',
                odcInstallation: 'DP-Check'
                
                // 2. Automatic Detection: Clean & Simple output
                script {
                    echo "#########################################################"
                    echo "             SECURITY SCAN: VULNERABLE LIBS              "
                    echo "#########################################################"
                    
                    // This command extracts only the library name from the XML
                    sh """
                    grep -B 15 '<vulnerability' dependency-check-report.xml | grep '<fileName>' | sed 's/<[^>]*>//g' | sed 's/^[[:space:]]*//' | sort -u
                    """
                    
                    echo "#########################################################"
                }
            }
        }
    }

    post {
        always {
            dependencyCheckPublisher pattern: '**/dependency-check-report.xml',
                                     failedTotalHigh: 0, 
                                     failedTotalCritical: 0
        }
        failure {
            echo "STOP: Critical vulnerabilities found in requirements.txt"
        }
    }
}
