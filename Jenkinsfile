pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    parameters {
        string(name: 'IMAGE_REPO', defaultValue: 'your-registry/flight-price-api', description: 'Docker image repo')
        string(name: 'IMAGE_TAG', defaultValue: 'latest', description: 'Docker image tag')
        string(name: 'KUBE_NAMESPACE', defaultValue: 'default', description: 'Kubernetes namespace')
    }

    environment {
        DOCKER_CREDENTIALS_ID = 'docker-registry-creds'
        KUBECONFIG_CREDENTIALS_ID = 'kubeconfig'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'python -m pip install --upgrade pip'
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Test') {
            steps {
                sh '''
                    if [ -d "tests" ]; then
                      pytest -q
                    else
                      echo "No tests directory found. Skipping tests."
                    fi
                '''
            }
        }

        stage('Build Image') {
            steps {
                sh 'docker build -t ${IMAGE_REPO}:${IMAGE_TAG} .'
            }
        }

        stage('Push Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: "${DOCKER_CREDENTIALS_ID}", usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh '''
                        echo "${DOCKER_PASS}" | docker login -u "${DOCKER_USER}" --password-stdin
                        docker push ${IMAGE_REPO}:${IMAGE_TAG}
                        docker logout
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                withCredentials([file(credentialsId: "${KUBECONFIG_CREDENTIALS_ID}", variable: 'KUBECONFIG_FILE')]) {
                    sh '''
                        export KUBECONFIG="${KUBECONFIG_FILE}"
                        kubectl apply -f k8s/deployment.yaml -n ${KUBE_NAMESPACE}
                        kubectl apply -f k8s/service.yaml -n ${KUBE_NAMESPACE}
                        kubectl apply -f k8s/hpa.yaml -n ${KUBE_NAMESPACE}
                        kubectl set image deployment/flight-price-api flight-price-api=${IMAGE_REPO}:${IMAGE_TAG} -n ${KUBE_NAMESPACE}
                        kubectl rollout status deployment/flight-price-api -n ${KUBE_NAMESPACE}
                    '''
                }
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}
