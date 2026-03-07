pipeline {
    agent any

    environment {
        // This makes sure tools are in the path
        SCANNER_HOME = tool 'SonarScanner'
    }

    stages {
        stage('Clone Repository') {
            steps {
                git 'https://github.com/walidchy/TP-Jenkins-Security.git'
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
                // Note: This requires a SonarQube server running. 
                // If you don't have one, this stage will fail unless you skip it.
                script {
                    try {
                        sh "${SCANNER_HOME}/bin/sonar-scanner -Dsonar.projectKey=TP-Jenkins"
                    } catch (Exception e) {
                        echo "SonarQube server not reachable, continuing..."
                    }
                }
            }
        }

        stage('SCA Scan (Dependency-Check)') {
            steps {
                // Step 10 & 11: Generate HTML and FAIL if CVSS score is above 7
                dependencyCheck additionalArguments: '--scan . --format HTML --failBuildOnCVSS 7', odcInstallation: 'DP-Check'
            }
        }
    }

    post {
        always {
            // Publishes the report to the Jenkins UI
            dependencyCheckPublisher pattern: '**/dependency-check-report.html'
        }
        failure {
            echo 'Build failed! Possible reasons: Test failure OR Critical Vulnerability (CVSS > 7)'
        }
    }
}
