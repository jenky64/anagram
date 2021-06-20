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
                sh 'ls -l'
                script {
                    echo "git commit: ${env.GIT_COMMIT}"
                    echo "git branch: ${env.GIT_BRANCH}"
                    echo "git url: ${env.GIT_URL}"
                    echo "git previous commit: ${env.GIT_PREVIOUS_COMMIT}"
                    echo "git author name: ${env.GIT_AUTHOR_NAME}"
                    echo "git author: ${env.GIT_AUTHOR_EMAIL}"
                    echo "job name: ${env.JOB_NAME}"
                    echo "job base name: ${env.JOB_BASE_NAME}"

                    def JOBPARTS = JOB_NAME.tokenize('/') as string[]
                    def JP1 =  JOBPARTS[0]
                    def JP2 = JOBPARTS[1]
                    echo "JP1 = ${JP1}"
                    echo "JP2 = ${JP2}"


                   echo "checking for repository branch volume directory..."
                    DIR=sh(returnStdout: true, script: 'pwd')
                    MKDIR = sh(returnStdout: true, script: "/usr/bin/python3 ${env.SCRIPT_DIR}/configure.py -d ${DIR}").trim()
                    echo "mkdir = ${MKDIR}"
                    if (MKDIR == 'true') {
                        echo "repository branch volume directory ${DIR} successfully created."
                    } else {
                        echo "repository branch volume directory ${DIR} already exists."
                    }



                    //DIR=sh(returnStdout: true, script: "echo ${env.GIT_URL} | cut -d'/' -f5 | cut -d'.' -f1").trim()
                    //DIR=sh(returnStdout: true, script: "echo /volumes/${DIR}/${GIT_BRANCH}/").trim()
                    echo "DIR = ${DIR}"
                }

            }
        }
    }
}