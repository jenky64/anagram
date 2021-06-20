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
                    env.JOBDIR = JOB_NAME.replace('/','_')
                    echo "JOBDIR = ${env.JOBDIR}"

                    echo "checking for repository branch volume directory..."
                    MKDIR = sh(returnStdout: true, script: "/usr/bin/python3 ${env.SCRIPT_DIR}/configure.py -d ${env.JOBDIR}").trim()
                    echo "mkdir = ${MKDIR}"
                    if (MKDIR == 'true') {
                        echo "repository branch volume directory ${env.JOBDIR} successfully created."
                    } else {
                        echo "repository branch volume directory ${env.JOBDIR} already exists."
                    }
                }
            }
        }
        stage("Next") {
            steps {
                script {
                    echo "volume directory = ${env.JOBDIR}"
                }
            }
        }
    }
}