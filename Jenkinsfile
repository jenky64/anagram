pipeline {
    agent any

    environment {
        BASE_DIR='/jenkins'
        SCRIPT_DIR="${env.BASE_DIR}/scripts"
        VOLUME_DIR='/volumes'
        REPO_NAME=""
        MKDIR=""
        VALID_IMAGE='false'
        REUSE='false'
        JOB_DIR=""
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

                    JOB_DIR = JOB_NAME.replace('/','_')
                    VOLUME_PATH = [VOLUME_DIR, JOB_DIR].join('/')
                    echo "JOB_DIR = ${JOB_DIR}"

                    echo "checking for repository branch volume directory..."
                    //MKDIR = sh(returnStdout: true, script: "/usr/bin/python3 ${env.SCRIPT_DIR}/configure.py -d ${JOB_DIR}").trim()
                    MKDIR = sh(returnStdout: true, script: "/usr/bin/python3 ${env.SCRIPT_DIR}/configure.py -d ${env.WORKSPACE}").trim()
                    echo "mkdir = ${MKDIR}"
                    if (MKDIR == 'true') {
                        echo "repository branch volume directory ${JOB_DIR} successfully created."
                        //sh 'cp dockerfile ${VOLUME_PATH}'
                        //sh 'cp modules-list.txt ${VOLUME_PATH}'
                        //sh 'cp testing-modules-list.txt ${VOLUME_PATH}'
                        //sh 'cp noxfile.py ${VOLUME_PATH}'
                    } else {
                        echo "repository branch volume directory ${JOB_DIR} already exists."
                    }
                }
            }
        }
        stage("Test") {
            steps {
                script {
                    echo "volume directory = ${JOB_DIR}"
                    echo "full path = ${VOLUME_PATH}"
                }
            }
        }
    }
}