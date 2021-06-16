pipeline {
    agent any

    environment {
        BASE_DIR='/jenkins'
        SCRIPT_DIR="${env.BASE_DIR}/scripts"
        VOLUME_DIR='/volumes'
        REPO_NAME=""
        MKDIR=""
        VALIDIMAGE='false'
        REUSE='false'
    }

    stages {
        stage("Configure") {
            steps {

                script {
                    echo "git commit: ${env.GIT_COMMIT}"
                    echo "git branch: ${env.GIT_BRANCH}"
                    echo "git url: ${env.GIT_URL}"
                    echo "git previous commit: ${env.GIT_PREVIOUS_COMMIT}"
                    echo "git author name: ${env.GIT_AUTHOR_NAME}"
                    echo "git author: ${env.GIT_AUTHOR_EMAIL}"
                    DIR=sh(returnStdout: true, script: "echo ${env.GIT_URL} | awk '-F/' '{print \\\$NF}' | cut -d'.' -f1").trim()
                    echo "DIR = ${DIR}"
                }

            }
        }
    }
}