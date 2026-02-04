# Jenkins CI/CD Pipeline

This repository includes a Jenkins pipeline (`Jenkinsfile`) that builds, tests, dockerizes, and deploys the flight price prediction API to Kubernetes.

## Prerequisites

- Jenkins agent with `docker`, `kubectl`, and `python` available
- Docker registry credentials in Jenkins
- Kubernetes `kubeconfig` stored as a Jenkins file credential

## Jenkins Credentials

Create these credentials in Jenkins:

- **`docker-registry-creds`**: Username/Password for your container registry
- **`kubeconfig`**: File credential containing a kubeconfig with access to your cluster

## Pipeline Parameters

- `IMAGE_REPO`: Docker image repo (e.g., `your-registry/flight-price-api`)
- `IMAGE_TAG`: Docker image tag (e.g., `latest` or `${BUILD_NUMBER}`)
- `KUBE_NAMESPACE`: Kubernetes namespace for deployment

## What the Pipeline Does

1. Install Python dependencies from `requirements.txt`
2. Run tests if a `tests/` directory exists
3. Build Docker image
4. Push image to registry
5. Deploy to Kubernetes using manifests in `k8s/`

## Notes

- Update `k8s/deployment.yaml` to match your registry if needed. The pipeline sets the image on deploy.
- If you want to skip tests, remove the `Test` stage or keep it as is.
