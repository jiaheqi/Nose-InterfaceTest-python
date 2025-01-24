#!groovy
pipeline {

    agent {
        label 'subor-slave'
    }

    stages {

        stage('Setup') {
            steps {
                sh '''
                virtualenv -p python3 .venv
                source .venv/bin/activate
                pip install pip --upgrade
                pip install -I --trusted-host nexus.youle.game -i http://nexus.youle.game/repository/pypi-public/simple -r requirements.txt
                '''
            }
        }

        stage('Run') {
            steps {
                sh '''
                export PYTHONPATH=${WORKSPACE}
                source .venv/bin/activate
                python main.py run
                '''
            }
        }

    }

    post {
        success {
            //当此Pipeline成功时打印消息
            sh '''
            echo "测试任务全部成功"
            '''
        }
        failure {
            //当此Pipeline失败时打印消息
            sh '''
            source .venv/bin/activate
            python main.py ding -r failure
            '''
        }
    }
}

