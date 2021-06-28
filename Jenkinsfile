pipeline {
    agent any

    environment {
        BASE_DIR='/jenkins'
        SCRIPT_DIR="${env.BASE_DIR}/scripts"
        VALID_IMAGE=0
        COMMIT_STATUS=1
        CHECKOUT_STATUS=1
        REVERT_STATUS=1
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

                    echo "checking for repository branch volume directory..."
                    MKDIR = sh(returnStdout: true, script: "/usr/bin/python3 ${env.SCRIPT_DIR}/configure.py -d ${env.WORKSPACE}").trim()
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
                    //echo "valid_image = ${VALID_IMAGE}"
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
                        echo "tests passed. saving commit tag."
                        SAVE_COMMIT = sh(returnStatus: true, script: "/usr/bin/python3 ${env.SCRIPT_DIR}/git/save_commit.py -c ${env.GIT_COMMIT} -d ${env.WORKSPACE}")
                        if (SAVE_COMMIT == 0) {
                            echo "commit tag save successful"
                        } else {
                            echo "commit tag save failed"
                        }
                    } else {
                        echo "tests failed. commit tag not saved. need to revert commit"
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
                    echo "reverting commit due to test failure..."
                    COMMIT = sh(returnStdout: true, script: "/usr/bin/python3 ${env.SCRIPT_DIR}/git/read_commit.py -d ${env.WORKSPACE}").trim()
                    if (COMMIT == 'false') {
                        echo "unable to read commit file. cannot revert commit. must be managed manually."
                    }
                    //REVERT_STATUS = sh(returnStatus: true, script: "git revert ${COMMIT} --no-edit")
                    REVERT_STATUS = sh(returnStatus: true, script: "git revert ${COMMIT}")
                    //COMMIT_STATUS = sh(returnStatus: true, script: "git commit -am 'reverting to clean state'")
                    COMMIT_STATUS = 0
                    CHECKOUT_STATUS = sh(returnStatus: true, script: "git checkout -b ${env.GIT_BRANCH}")
                    echo "REVERT_STATUS = ${REVERT_STATUS}"
                    echo "COMMIT_STATUS = ${COMMIT_STATUS}"
                    echo "CHECKOUT_status = ${CHECKOUT_STATUS}"
                    //if (REVERT_STATUS == 0 && CHECKOUT_STATUS == 0) {
                  /*  if (COMMIT_STATUS == 0 && CHECKOUT_STATUS == 0) {
                        GIT_PUSH = sh(returnStatus: true, script: "git push origin ${env.GIT_BRANCH}")
                        if (GIT_PUSH == 0) {
                            echo "git revert successful. previous state will be validated in next run."
                            GIT_DELETE = sh(returnStatus: true, script: "git branch -d ${env.GIT_BRANCH}")
                        } else {
                            echo "git revert failed on git push to branch. must be managed manually"
                        }
                    } */
                }
            }
        }
       stage("PushAfterRevert") {
            when {
                expression {
                    COMMIT_STATUS == 0 && CHECKOUT_STATUS == 0
                }
            }
            steps {
                script {
                    echo "testing push after revert"
                    //GIT_DELETE = sh(returnStatus: true, script: "git branch -d ${env.GIT_BRANCH}")
                    //echo "git delete = ${GIT_DELETE}"
                }
            }
        }
    }
}