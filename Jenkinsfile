pipeline {
    agent any

    environment {
        BASE_DIR='/jenkins'
        SCRIPT_DIR="${env.BASE_DIR}/scripts"
        VOLUME_DIR='/volumes'
        REPO_NAME=""
        MKDIR=""
        VALID_IMAGE='false'
        BUILD_IMAGE='true'
        REUSE='false'
        JOB_DIR=""
        VOLUME_PATH=""
    }

    stages {
        /* stage("Configure") {
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
                    MKDIR = sh(returnStdout: true, script: "/usr/bin/python3 ${env.SCRIPT_DIR}/configure.py -d ${env.WORKSPACE}").trim()
                    echo "mkdir = ${MKDIR}"
                    if (MKDIR == 'true') {
                        echo "repository branch volume directory ${JOB_DIR} successfully created."
                    } else {
                        echo "repository branch volume directory ${JOB_DIR} already exists."
                    }
                }
            }
        }
        stage("DockerCheck") {
            steps {
                script {
                    echo "validating docker image..."
                    VALID_IMAGE = sh(returnStdout: true, script: "/usr/bin/python3 ${env.SCRIPT_DIR}/validate.py -d ${env.WORKSPACE}").trim()
                    echo "valid_image = ${VALID_IMAGE}"
                    if (VALID_IMAGE == 'true') {
                        echo "Docker image validation passed."
                    } else {
                        echo "Docker image validation failed. Rebuild required."
                    }
                }
            }
        } */
        stage("DockerRebuild") {
            when {
                expression {
                    VALID_IMAGE == 'false'
                }
            }
            steps {
                script {
                    echo "Rebuilding docker image..."
                    echo "Running tests..."
                    echo "workspace = ${env.WORKSPACE}"
                    BUILD_IMAGE = sh(returnStdout: true, script: "/usr/bin/python3 ${env.SCRIPT_DIR}/docker1.py -b -d ${env.WORKSPACE}").trim()
                    echo "build_image = ${BUILD_IMAGE}"
                    if (BUILD_IMAGE == 'true') {
                        echo "Docker image rebuild passed."
                    } else {
                        echo "Docker image rebuild failed.."
                    }
                }
            }
        }
        stage("RunTests") {
            steps {
                script {
                    echo "running tests"
                }
            }
        }
    }
}