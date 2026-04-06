# Kubernetes Manifests

This folder deploys the prediction API in a Kubernetes cluster.

## Files

- `deployment.yaml` - Deployment with probes and resource limits.
- `service.yaml` - ClusterIP service exposing port 80.
- `hpa.yaml` - Autoscaling based on CPU utilization.
- `ingress.yaml` - Ingress routing for the API.

## Usage

Update the image name in `deployment.yaml`:

- `image: your-registry/flight-price-api:latest`

Apply manifests:

- `kubectl apply -f k8s/deployment.yaml`
- `kubectl apply -f k8s/service.yaml`
- `kubectl apply -f k8s/hpa.yaml`
- `kubectl apply -f k8s/ingress.yaml`

If you use the provided ingress, map `flight-price.local` to `127.0.0.1` in your hosts
file and ensure an ingress controller (e.g., nginx) is installed.
