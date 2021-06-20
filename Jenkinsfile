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
        JOBDIR=""
        VOLUME_PATH=""
    }

    stages {
        stage("Configure") {
            steps {
                sh 'ls -l'
                script {
                    echo "git commit: ${env.GIT_COMMIT}"
                    echo "git branch: ${env.GIT_BRANCH}"
                    echo "git url: ${env.GIT_URL}"
                    echo "git previous commit: ${env.GIT_PREVIOUS_COMMIT}"

                    //def JOBDIR = JOB_NAME.replace('/','_')
                    JOBDIR = JOB_NAME.replace('/','_')
                    VOLUME_PATH = [VOLUME_DIR, JOBDIR].join('/')
                    echo "JOBDIR = ${JOBDIR}"

                    echo "checking for repository branch volume directory..."
                    MKDIR = sh(returnStdout: true, script: "/usr/bin/python3 ${env.SCRIPT_DIR}/configure.py -d ${JOBDIR}").trim()
                    echo "mkdir = ${MKDIR}"
                    if (MKDIR == 'true') {
                        echo "repository branch volume directory ${JOBDIR} successfully created."
                    } else {
                        echo "repository branch volume directory ${JOBDIR} already exists."
                    }
                }
            }
        }
        stage("Next") {
            steps {
                script {
                    echo "volume directory = ${JOBDIR}"
                    echo "full path = ${VOLUME_PATH}"
                }
            }
        }
    }
}