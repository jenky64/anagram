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

                    JOB_DIR = JOB_NAME.replace('/','_')
                    //VOLUME_PATH = [VOLUME_DIR, JOB_DIR].join('/')

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
                        SAVE_COMMIT = sh(returnStatus: true, script: "/usr/bin/python3 ${env.SCRIPT_DIR}/git/save_commit.py -c ${env.GIT_COMMIT} -d ${env.WORKSPACE}")
                        if (SAVE_COMMIT == 0) {
                            echo "commit save successful"
                        } else {
                            echo "commit save failed"
                        }
                    } else {
                        echo "tests failed. need to revert commit"
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
                    COMMIT = sh(returnStdout: true, script: "/usr/bin/python3 ${env.SCRIPT_DIR}/git/read_commit.py -d ${env.WORKSPACE}").trim()
                    REVERT_STATUS = sh(returnStatus: true, script: "git revert ${COMMIT} --no-edit")
                    echo "REVERT_status = ${REVERT_STATUS}"
                    CHECKOUT_STATUS = sh(returnStatus: true, script: "git branch -b ${env.GIT_BRANCH}")
                    echo "CHECKOUT_status = ${CHECKOUT_STATUS}"
                    //if (REVERT_STATUS == 0 && CHECKOUT_STATUS == 0) {
                    if (REVERT_STATUS == 0 && CHECKOUT_STATUS == 0) {
                        sh 'git push ${env.GIT_BRANCH}'
                    }
                }
            }
        }
    }
}