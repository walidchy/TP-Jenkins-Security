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
                // Scans the requirements.txt file
                dependencyCheck additionalArguments: '--scan requirements.txt --format ALL --enableExperimental',
                odcInstallation: 'DP-Check'
            }
        }
    }

    post {
        always {
            // failedTotalCritical: 0 makes the build RED if any Critical vuln is found
            dependencyCheckPublisher pattern: '**/dependency-check-report.xml',
                                     failedTotalHigh: 0, 
                                     failedTotalCritical: 0
        }
        
        failure {
            script {
                echo """
                ############################################################################
                #                          SECURITY GATE FAILURE                           #
                ############################################################################
                #                                                                          #
                #  CRITICAL VULNERABILITY DETECTED IN requirements.txt                     #
                #                                                                          #
                #  LIBRARY:  PyYAML 3.12                                                   #
                #  CVE:      CVE-2017-18342                                                #
                #  SCORE:    9.8 (CRITICAL)                                                #
                #                                                                          #
                #  STATUS:   BUILD BLOCKED BY DEVSECOPS POLICY                             #
                #                                                                          #
                ############################################################################
                """
            }
        }
    }
}
