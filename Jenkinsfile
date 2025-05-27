pipeline {
    agent any

    environment {
        BUILD_ID = "${env.BUILD_ID}"
        BASE_DIAGRAM_NAME = "api_interaction_diagram"
    }

    stages {
        stage('Setup Environment') {
            steps {
                sh 'python3 --version'
                sh 'pip3 install --upgrade pip'
                sh 'pip3 install -r requirements.txt'
            }
        }

        stage('Generate PlantUML File') {
            steps {
                sh 'python3 -m src.main'
            }
        }

        stage('Render Diagram') {
            steps {
                script {
                    def uniquePumlFile = "diagrams/${env.BASE_DIAGRAM_NAME}_${env.BUILD_ID}.puml"
                    def uniquePngFile = "diagrams/${env.BASE_DIAGRAM_NAME}_${env.BUILD_ID}.png"

                    if (fileExists(uniquePumlFile)) {
                        sh "docker run --rm -v $(pwd):/src plantuml/plantuml:1.2024.5 java -jar /plantuml.jar -tpng /src/${uniquePumlFile} -o /src/diagrams/"
                    } else {
                        error "ERROR: ${uniquePumlFile} not found. Cannot render diagram. Check 'Generate PlantUML File' stage logs."
                    }
                }
            }
        }

        stage('Archive Artifacts') {
            steps {
                script {
                    def uniquePumlFile = "diagrams/${env.BASE_DIAGRAM_NAME}_${env.BUILD_ID}.puml"
                    def uniquePngFile = "diagrams/${env.BASE_DIAGRAM_NAME}_${env.BUILD_ID}.png"
                    archiveArtifacts artifacts: "${uniquePumlFile}, ${uniquePngFile}", fingerprint: true
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline finished successfully!.'
        }
        failure {
            echo 'Pipeline failed!.'
        }
    }
}