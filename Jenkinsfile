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
                // 1. Run the scan and generate the XML report
                dependencyCheck additionalArguments: '--scan requirements.txt --format ALL --enableExperimental',
                odcInstallation: 'DP-Check'
                
                // 2. AUTOMATIC DETECTION: Parse the XML to find vulnerable library names
                script {
                    echo "#########################################################"
                    echo "      AUTOMATIC VULNERABILITY DETECTION RESULTS         "
                    echo "#########################################################"
                    
                    // This command looks into the XML and finds the <fileName> of every vulnerable dependency
                    sh """
                    grep -B 3 "vulnerability" dependency-check-report.xml | grep "fileName" | sed 's/.*<fileName>\\(.*\\)<\\/fileName>.*/[!] VULNERABLE LIBRARY FOUND: \\1/' | sort -u
                    """
                    
                    echo "#########################################################"
                }
            }
        }
    }

    post {
        always {
            // failedTotalHigh: 0 forces the build to be RED if any risk is found
            dependencyCheckPublisher pattern: '**/dependency-check-report.xml',
                                     failedTotalHigh: 0, 
                                     failedTotalCritical: 0
        }
        
        failure {
            echo "FAILED: The Security Gate has blocked this build because of the libraries listed above."
        }
    }
}
