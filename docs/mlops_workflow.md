# MLOps Workflow Guide

This document describes the workflow for each stage of the MLOps lifecycle in this project and where to capture supporting screenshots.

> Place screenshots under `docs/images/` using the filenames listed in each section.

To regenerate **all** workflow placeholder PNGs in one step (from the repo root, with dependencies installed):

`python scripts/generate_doc_images.py`

## REST API

**Goal:** Serve predictions for flight price and user gender models.

**Workflow**

1. Train models (or ensure artifacts exist):
   - `python src/training/train_model.py`
   - `python src/training/train_gender_model.py`
2. Start the API:
   - `python src/api/app.py`
3. Validate health:
   - `GET /health`
4. Submit predictions:
   - `POST /predict`
   - `POST /predict_gender`

**Screenshot**

- `docs/images/rest_api_health.png` (health response in browser or Postman)
- `docs/images/rest_api_predict.png` (prediction request/response)

## Streamlit App

**Goal:** Visualize user profile, booking history, recommendations, and insights.

**Workflow**

1. Start the app:
   - `streamlit run streamlit_app.py`
2. Train recommender if prompted.
3. Select a user and review recommendations and charts.

**Screenshot**

- `docs/images/streamlit_home.png` (main UI with user selection)
- `docs/images/streamlit_insights.png` (insights charts section)

## Docker Deployment

**Goal:** Package and run the API in a container with auto-training when artifacts are missing.

**Workflow**

1. Build image:
   - `docker build -t flight-price-api .`
2. Run container:
   - `docker run -p 5000:5000 flight-price-api`
3. Verify health endpoint in the container.

**Screenshot**

- `docs/images/docker_build.png` (build output)
- `docs/images/docker_run_health.png` (container running + health check)

## Kubernetes Deployment

**Goal:** Deploy the API for scalable, resilient serving.

**Workflow**

1. Update image in `k8s/deployment.yaml`.
2. Apply manifests:
   - `kubectl apply -f k8s/deployment.yaml`
   - `kubectl apply -f k8s/service.yaml`
   - `kubectl apply -f k8s/hpa.yaml`
3. Validate pods and service:
   - `kubectl get pods`
   - `kubectl get svc`

**Screenshot**

- `docs/images/k8s_pods.png` (pods running)
- `docs/images/k8s_service.png` (service details)
- `docs/images/k8s_hpa.png` (HPA status)

## Scheduling in Airflow

**Goal:** Automate validation and training using a DAG.

**Workflow**

1. Ensure Airflow can import `src/` (DAG appends the path).
2. Configure:
   - `FLIGHT_DATA_PATH`
   - `FLIGHT_ARTIFACTS_DIR`
3. Enable the DAG: `flight_price_training_pipeline`
4. Trigger and monitor runs.

**Screenshot**

- `docs/images/airflow_dag.png` (DAG view)
- `docs/images/airflow_run.png` (task run status)

## CI/CD Pipeline (Jenkins)

**Goal:** Build, test, containerize, and deploy automatically.

**Workflow**

1. Configure Jenkins credentials:
   - `docker-registry-creds`
   - `kubeconfig`
2. Run the `Jenkinsfile` pipeline.
3. Confirm image push and Kubernetes deploy stages.

**Screenshot**

- `docs/images/jenkins_pipeline.png` (pipeline stages)
- `docs/images/jenkins_deploy.png` (deploy stage output)

## MLflow Tracking

**Goal:** Track experiments, metrics, and model artifacts.

**Workflow**

1. Train models via:
   - `src/training/train_model.py`
   - `src/training/train_gender_model.py`
2. Open MLflow UI:
   - `mlflow ui --backend-store-uri sqlite:///mlflow.db`
3. Inspect metrics and artifacts.

**Screenshot**

- `docs/images/mlflow_runs.png` (run list and metrics)
- `docs/images/mlflow_artifacts.png` (artifact view)


