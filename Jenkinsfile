
pipeline {
    agent {
            label 'load-test'
        }
    parameters {

            choice( name: 'SERVER_STATUS',
                    choices: ['Start','Restart', 'Stop'],
                    description: 'Please choose if you would like to Start/Restart/Stop the server')
        }
    stages {
        stage('Completing Task') {
            steps {
                echo "Server Status : ${params.SERVER_STATUS}"
                script {
                    if ("${params.SERVER_STATUS}" == 'Start'){
                        echo "Starting Server"
                        sh """
                            cd hoverfly_stub
                            JENKINS_NODE_COOKIE=dontKillMe ./start_stub_server.sh
                        """
                    }
                    else if ("${params.SERVER_STATUS}" == 'Stop'){
                        echo "Stopping Server"
                        sh """
                            cd hoverfly_stub
                            ./stop_stub_server.sh
                        """
                    }
                    else {
                        echo "Restarting Server"
                        sh """
                            cd hoverfly_stub
                            JENKINS_NODE_COOKIE=dontKillMe ./restart_stub_server.sh
                        """
                    }
                }
            }
        }
    }
}