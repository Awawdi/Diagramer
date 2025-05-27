pipeline {
    agent any

    stages {

        stage('Generate PlantUML') {
            steps {
                script {
                    sh 'python3 -m src.api_call_generator'
                }
            }
        }

        stage('Render Diagram') {
            steps {
                script {
                    if (fileExists('diagrams/api_interaction_diagram.puml')) {
                        sh 'docker run --rm -v $(pwd):/src plantuml/plantuml:1.2024.5 java -jar /plantuml.jar -tpng /src/diagrams/api_interaction_diagram.puml -o /src/diagrams/'
                        echo 'PlantUML diagram rendered successfully.'
                    } else {
                        error 'ERROR: api_interaction_diagram.puml not found. Cannot render diagram.'
                    }
                }
            }
        }

        stage('Archive Artifacts') {
            steps {
                archiveArtifacts artifacts: 'diagrams/*.puml, diagrams/*.png', fingerprint: true
            }
        }
    }

    post {
        success {
            echo 'Pipeline finished successfully!'
        }
        failure {
            echo 'Pipeline failed. Check logs for details.'
        }
    }
}