# ML Productionization

This repository contains a multi-component MLOps project for travel data. It includes model training, a prediction API, a recommender system with a Streamlit UI, Airflow automation, containerization, Kubernetes deployment, and Jenkins CI/CD.

## Repository Structure

- `src/api/` - Flask API for flight price and gender prediction.
- `src/training/` - Training scripts for regression and classification models.
- `src/recommendation/` - Hotel recommender utilities and training entrypoint.
- `streamlit_app.py` - Streamlit interface for recommendations and insights.
- `dags/` - Airflow DAG for scheduled training.
- `k8s/` - Kubernetes deployment, service, and HPA manifests.
- `jenkins/` - Jenkins pipeline documentation.
- `project_overview.md` - Business context and objectives.

Each component has a dedicated README/user guide:

- API: `src/api/README.md`
- Training: `src/training/README.md`
- Recommendation: `src/recommendation/README.md`
- Airflow: `dags/README.md`
- Kubernetes: `k8s/README.md`
- Streamlit: `docs/streamlit_app.md`
- Jenkins: `jenkins/README.md`

## Data Setup

Place the datasets in `travel_capstone/`:

- `travel_capstone/flights.csv`
- `travel_capstone/users.csv`
- `travel_capstone/hotels.csv`

## Quickstart (local)

1. Install dependencies:
   - `pip install -r requirements.txt`
2. Train models:
   - `python src/training/train_model.py`
   - `python src/training/train_gender_model.py`
3. Run the API:
   - `python src/api/app.py`
4. Run the Streamlit app:
   - `streamlit run streamlit_app.py`

## Containerized Run

Use the Docker image to build and run the API with model auto-training:

- `docker build -t flight-price-api .`
- `docker run -p 5000:5000 flight-price-api`

The `start.sh` script trains missing models if the datasets exist.

## MLflow Tracking

MLflow uses `mlflow.db` by default. Override with:

- `MLFLOW_TRACKING_URI`
- `MLFLOW_EXPERIMENT`
