pipeline {
    agent any

    environment {
        BASE_DIR='/jenkins'
        SCRIPT_DIR="${env.BASE_DIR}/scripts"
        VOLUME_DIR='/volumes'
        MKDIR=""
        VALID_IMAGE=0
        BUILD=0
        JOB_DIR=""
        VOLUME_PATH=""
    }

    stages {
        stage("Configure") {
            steps {
                script {
                    echo "git branch: ${env.GIT_BRANCH}"
                    echo "git url: ${env.GIT_URL}"
                    echo "git commit: ${env.GIT_COMMIT}"
                    echo "git previous commit: ${env.GIT_PREVIOUS_COMMIT}"

                    //JOB_DIR = JOB_NAME.replace('/','_')
                    //VOLUME_PATH = [VOLUME_DIR, JOB_DIR].join('/')

                  /*  echo "checking for repository branch volume directory..."
                    MKDIR = sh(returnStdout: true, script: "/usr/bin/python3 ${env.SCRIPT_DIR}/configure.py -d ${env.WORKSPACE}").trim()
                    echo "mkdir = ${MKDIR}"
                    if (MKDIR == 'true') {
                        echo "repository branch volume directory ${JOB_DIR} successfully created."
                    } else {
                        echo "repository branch volume directory ${JOB_DIR} already exists."
                    } */
                }
            }
        }
        stage("ValidateDockerImage") {
            steps {
                script {
                    echo "validating docker image..."
                    VALID_IMAGE = sh(returnStatus: true, script: "/usr/bin/python3 ${env.SCRIPT_DIR}/docker/validate.py -d ${env.WORKSPACE}")
                    echo "valid_image = ${VALID_IMAGE}"
                    if (VALID_IMAGE == 0) {
                        echo "Docker image validation passed."
                    } else {
                        echo "Docker image validation failed. Rebuild required."
                    }
                }
            }
        }
        stage("DockerRebuild") {
            when {
                expression {
                    VALID_IMAGE == 1
                }
            }
            steps {
                script {
                    echo "Rebuilding docker image..."
                    BUILD = sh(returnStatus: true, script: "/usr/bin/python3 ${env.SCRIPT_DIR}/docker/build.py -d ${env.WORKSPACE} -t l2lcommit:latest")
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
                    RET = sh(returnStatus: true, script: "/usr/bin/python3 ${env.SCRIPT_DIR}/docker/run.py -d ${env.WORKSPACE} -i l2lcommit:latest")
                    echo "ret = ${RET}"
                    if (RET == 0) {
                        echo "tests passed"
                    } else {
                        echo "tests failed"
                    }
                }
            }
        }
        stage("CommitRevert") {
            when {
                expression {
                    RET != 0
                }
            }
            steps {
                script {
                    echo "reverting latest commit due to test failure..."
                    REVERT_STATUS = sh(returnStatus: true, script: "git revert ${env.GIT_COMMIT} --no-edit")
                    COMMIT_STATUS = sh(returnStatus: true, script: "git commit -m 'commit ${env.GIT_COMMIT} reverted'")
                    echo "commit_status = ${COMMIT_STATUS}"
                    if (REVERT_STATUS == 0) {
                        sh 'git push origin dev'
                    }
                }
            }
        }
    }
}