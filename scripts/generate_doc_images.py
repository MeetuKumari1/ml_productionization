"""Generate all documentation PNGs under docs/images/ (see docs/mlops_workflow.md).

Run from repo root:
    .venv\\Scripts\\python.exe scripts\\generate_doc_images.py
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import patches

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "images"


def _save(fig: plt.Figure, name: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / name
    fig.savefig(path, dpi=120, bbox_inches="tight", facecolor="#f0f2f5")
    plt.close(fig)
    print(f"Wrote {path.relative_to(ROOT)}")


def _browser_chrome(ax, y_top: float, url: str, width: float = 11.0) -> None:
    ax.add_patch(patches.Rectangle((0.15, y_top - 0.55), width, 0.5, facecolor="#dee1e6", edgecolor="#ccc"))
    ax.add_patch(patches.Rectangle((0.35, y_top - 0.38), width - 0.5, 0.28, facecolor="white", edgecolor="#bbb"))
    ax.text(0.45, y_top - 0.24, url, fontsize=8, color="#333", family="monospace")


def fig_rest_api_health() -> None:
    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.5)
    ax.axis("off")
    _browser_chrome(ax, 5.35, "http://127.0.0.1:5000/health")
    ax.add_patch(patches.Rectangle((0.15, 0.35), 9.7, 4.55, facecolor="white", edgecolor="#ccc"))
    ax.text(0.28, 4.75, "GET /health", fontsize=9, fontweight="bold", color="#333")
    body = """{
  "features": ["time", "distance", "day_of_week", "month"],
  "gender_features": ["age", "estimated_salary"],
  "gender_model_loaded": true,
  "gender_model_name": "LogisticRegression",
  "model_loaded": true,
  "model_name": "RandomForest",
  "status": "ok"
}"""
    ax.text(0.28, 4.45, body, fontsize=8, color="#1a1a1a", family="monospace", va="top")
    _save(fig, "rest_api_health.png")


def fig_rest_api_predict() -> None:
    fig, ax = plt.subplots(figsize=(11, 5.2))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 5.2)
    ax.axis("off")
    ax.text(0.2, 4.85, "POST /predict (Postman or curl)", fontsize=10, fontweight="bold", color="#212529")

    ax.add_patch(patches.Rectangle((0.15, 0.35), 5.2, 4.25, facecolor="white", edgecolor="#0d6efd", linewidth=1.5))
    ax.text(0.28, 4.35, "Request JSON", fontsize=9, fontweight="bold", color="#0d6efd")
    req = """{
  "time": 120,
  "distance": 800,
  "day_of_week": 3,
  "month": 6
}"""
    ax.text(0.28, 4.05, req, fontsize=8, family="monospace", va="top", color="#333")

    ax.add_patch(patches.Rectangle((5.55, 0.35), 5.3, 4.25, facecolor="#f8fff8", edgecolor="#198754", linewidth=1.5))
    ax.text(5.68, 4.35, "Response", fontsize=9, fontweight="bold", color="#198754")
    resp = """{
  "predictions": [245.32]
}"""
    ax.text(5.68, 4.05, resp, fontsize=8, family="monospace", va="top", color="#333")
    _save(fig, "rest_api_predict.png")


def fig_streamlit_home() -> None:
    fig, ax = plt.subplots(figsize=(10.5, 6))
    ax.set_xlim(0, 10.5)
    ax.set_ylim(0, 6)
    ax.axis("off")
    ax.add_patch(patches.Rectangle((0, 0), 2.4, 6, facecolor="#fafafa", edgecolor="#ddd"))
    ax.text(0.25, 5.65, "Streamlit", fontsize=10, fontweight="bold")
    ax.text(0.25, 5.15, "Select user", fontsize=8, color="#666")
    ax.add_patch(patches.Rectangle((0.25, 4.55), 1.9, 0.4, facecolor="#e8f4ff", edgecolor="#0d6efd"))
    ax.text(0.35, 4.75, "User ID: 42", fontsize=8)

    ax.add_patch(patches.Rectangle((2.5, 0), 8, 6, facecolor="white", edgecolor="#ddd"))
    ax.text(2.7, 5.65, "Travel insights", fontsize=12, fontweight="bold")
    ax.text(2.7, 5.2, "Profile summary and booking history for the selected user.", fontsize=9, color="#555")
    ax.add_patch(patches.Rectangle((2.7, 3.4), 7.5, 1.55, facecolor="#f8f9fa", edgecolor="#eee"))
    ax.text(2.85, 4.7, "[Recommendations panel]", fontsize=9, color="#888")
    _save(fig, "streamlit_home.png")


def fig_streamlit_insights() -> None:
    fig, ax = plt.subplots(figsize=(10.5, 6))
    ax.set_xlim(0, 10.5)
    ax.set_ylim(0, 6)
    ax.axis("off")
    ax.text(0.25, 5.65, "Insights", fontsize=12, fontweight="bold")
    for i, (title, y) in enumerate([("Bookings over time", 4.5), ("Spend by category", 2.4)]):
        ax.add_patch(patches.Rectangle((0.25, y - 1.55), 4.9, 1.45, facecolor="white", edgecolor="#dee2e6"))
        ax.text(0.4, y - 0.25, title, fontsize=9, fontweight="bold")
        ax.plot([0.5, 1.5, 2.5, 3.5, 4.5], [y - 0.55, y - 0.85, y - 0.6, y - 0.9, y - 0.5], color="#0d6efd", linewidth=2)
    ax.add_patch(patches.Rectangle((5.35, 0.85), 4.9, 4.35, facecolor="white", edgecolor="#dee2e6"))
    ax.text(5.5, 4.95, "Hotel recommendations", fontsize=9, fontweight="bold")
    ax.bar([5.6, 6.2, 6.8, 7.4], [0.8, 1.2, 0.6, 0.9], width=0.45, color=["#6f42c1", "#d63384", "#fd7e14", "#20c997"])
    _save(fig, "streamlit_insights.png")


def fig_docker_build() -> None:
    fig, ax = plt.subplots(figsize=(10.5, 6.5))
    ax.set_xlim(0, 10.5)
    ax.set_ylim(0, 6.5)
    ax.axis("off")
    ax.add_patch(patches.Rectangle((0.1, 0.1), 10.3, 6.3, facecolor="#1e1e1e", edgecolor="none"))
    lines = [
        "$ docker build -t flight-price-api .",
        " => [internal] load build definition from Dockerfile",
        " => transferring dockerfile: 512B",
        " => [internal] load .dockerignore",
        " => [1/6] FROM docker.io/library/python:3.12-slim",
        " => [2/6] WORKDIR /app",
        " => [3/6] COPY requirements.txt .",
        " => [4/6] RUN pip install --no-cache-dir -r requirements.txt",
        " => [5/6] COPY . .",
        " => [6/6] RUN chmod +x start.sh",
        " => exporting to image",
        " => => naming to docker.io/library/flight-price-api:latest",
        "Successfully tagged flight-price-api:latest",
    ]
    y = 6.05
    for line in lines:
        color = "#4ec9b0" if line.startswith("$") else "#d4d4d4"
        ax.text(0.2, y, line, fontsize=7.5, color=color, family="monospace", va="top")
        y -= 0.38
    _save(fig, "docker_build.png")


def fig_docker_run_health() -> None:
    fig, ax = plt.subplots(figsize=(10.5, 6.2))
    ax.set_xlim(0, 10.5)
    ax.set_ylim(0, 6.2)
    ax.axis("off")
    ax.add_patch(patches.Rectangle((0.1, 0.1), 10.3, 5.95, facecolor="#1e1e1e", edgecolor="none"))
    txt = """$ docker run -d -p 5000:5000 --name api flight-price-api
a1b2c3d4e5f6

$ docker ps --filter name=api
CONTAINER ID   IMAGE              STATUS         PORTS
a1b2c3d4e5f6   flight-price-api   Up 2 minutes   0.0.0.0:5000->5000/tcp

$ curl -s http://127.0.0.1:5000/health
{"gender_model_loaded":true,"model_loaded":true,"status":"ok"}"""
    y = 5.75
    for line in txt.split("\n"):
        c = "#4ec9b0" if line.startswith("$") else "#ce9178" if line.startswith("{") else "#d4d4d4"
        ax.text(0.2, y, line, fontsize=7.5, color=c, family="monospace", va="top")
        y -= 0.36
    _save(fig, "docker_run_health.png")


def fig_k8s_pods() -> None:
    fig, ax = plt.subplots(figsize=(10.5, 4.2))
    ax.set_xlim(0, 10.5)
    ax.set_ylim(0, 4.2)
    ax.axis("off")
    ax.add_patch(patches.Rectangle((0.1, 0.1), 10.3, 4.0, facecolor="#1e1e1e", edgecolor="none"))
    block = """$ kubectl get pods -n default
NAME                               READY   STATUS    RESTARTS   AGE
flight-price-api-7d9f8b6c5-xxxxx   1/1     Running   0          3m"""
    y = 3.75
    for line in block.split("\n"):
        ax.text(0.2, y, line, fontsize=8, color="#d4d4d4", family="monospace", va="top")
        y -= 0.42
    _save(fig, "k8s_pods.png")


def fig_k8s_service() -> None:
    fig, ax = plt.subplots(figsize=(10.5, 4.0))
    ax.set_xlim(0, 10.5)
    ax.set_ylim(0, 4)
    ax.axis("off")
    ax.add_patch(patches.Rectangle((0.1, 0.1), 10.3, 3.8, facecolor="#1e1e1e", edgecolor="none"))
    block = """$ kubectl get svc -n default
NAME               TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)
flight-price-api   ClusterIP   10.96.100.22    <none>        5000/TCP"""
    y = 3.55
    for line in block.split("\n"):
        ax.text(0.2, y, line, fontsize=8, color="#d4d4d4", family="monospace", va="top")
        y -= 0.42
    _save(fig, "k8s_service.png")


def fig_k8s_hpa() -> None:
    fig, ax = plt.subplots(figsize=(10.5, 4.0))
    ax.set_xlim(0, 10.5)
    ax.set_ylim(0, 4)
    ax.axis("off")
    ax.add_patch(patches.Rectangle((0.1, 0.1), 10.3, 3.8, facecolor="#1e1e1e", edgecolor="none"))
    block = """$ kubectl get hpa -n default
NAME               REFERENCE                     TARGETS         MINPODS   MAXPODS
flight-price-api   Deployment/flight-price-api   cpu: 15%/70%    1         5"""
    y = 3.55
    for line in block.split("\n"):
        ax.text(0.2, y, line, fontsize=7.5, color="#d4d4d4", family="monospace", va="top")
        y -= 0.42
    _save(fig, "k8s_hpa.png")


def fig_airflow_dag() -> None:
    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.5)
    ax.axis("off")
    ax.add_patch(patches.Rectangle((0, 5.0), 10, 0.5, facecolor="#017cee", edgecolor="none"))
    ax.text(0.3, 5.25, "DAG: flight_price_training_pipeline", color="white", fontsize=11, fontweight="bold", va="center")
    boxes = [("validate_data", 1.2, 2.8), ("train_model", 5.5, 2.8)]
    for label, x, y in boxes:
        ax.add_patch(patches.FancyBboxPatch((x, y), 2.6, 0.85, boxstyle="round,pad=0.05", facecolor="#00c292", edgecolor="#059669"))
        ax.text(x + 1.3, y + 0.42, label, ha="center", va="center", fontsize=9, color="white", fontweight="bold")
    ax.annotate("", xy=(5.4, 3.22), xytext=(3.9, 3.22), arrowprops=dict(arrowstyle="->", color="#555", lw=2))
    _save(fig, "airflow_dag.png")


def fig_airflow_run() -> None:
    fig, ax = plt.subplots(figsize=(10, 5.2))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.2)
    ax.axis("off")
    ax.text(0.25, 4.85, "Grid — manual run", fontsize=10, fontweight="bold")
    ax.add_patch(patches.Rectangle((0.2, 3.85), 9.6, 0.55, facecolor="#e7f1ff", edgecolor="#0d6efd"))
    ax.text(0.35, 4.18, "validate_data", fontsize=9, fontweight="bold", color="#0a58ca")
    ax.text(8.2, 4.18, "success", fontsize=8, color="#198754", fontweight="bold")

    ax.add_patch(patches.Rectangle((0.2, 3.15), 9.6, 0.55, facecolor="#e7f1ff", edgecolor="#0d6efd"))
    ax.text(0.35, 3.48, "train_model", fontsize=9, fontweight="bold", color="#0a58ca")
    ax.text(8.2, 3.48, "success", fontsize=8, color="#198754", fontweight="bold")

    ax.text(0.25, 2.65, "Task log (excerpt)", fontsize=9, fontweight="bold", color="#333")
    ax.add_patch(patches.Rectangle((0.2, 0.35), 9.6, 2.15, facecolor="#1e1e1e", edgecolor="#ccc"))
    log = """[2026-04-11] INFO — Running training pipeline
[2026-04-11] INFO — Best model RMSE logged to MLflow
[2026-04-11] INFO — Done. Returned value was recorded."""
    y = 2.25
    for line in log.split("\n"):
        ax.text(0.35, y, line, fontsize=7.5, color="#9cdcfe", family="monospace", va="top")
        y -= 0.32
    _save(fig, "airflow_run.png")


def fig_jenkins_pipeline() -> None:
    fig, ax = plt.subplots(figsize=(11, 3.8))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 3.8)
    ax.axis("off")
    ax.text(0.2, 3.45, "Stage View — build #12", fontsize=10, fontweight="bold")
    stages = [
        ("Checkout", 12),
        ("Install Deps", 45),
        ("Test", 28),
        ("Build Image", 120),
        ("Push Image", 34),
        ("Deploy", 56),
    ]
    x0 = 0.25
    w = 1.55
    for i, (name, sec) in enumerate(stages):
        x = x0 + i * (w + 0.12)
        ax.add_patch(patches.Rectangle((x, 1.5), w, 1.35, facecolor="#28a745", edgecolor="#1e7e34"))
        ax.text(x + w / 2, 2.45, name, ha="center", va="center", fontsize=7, color="white", fontweight="bold")
        ax.text(x + w / 2, 1.85, f"{sec}s", ha="center", fontsize=7, color="#e8f5e9")
    _save(fig, "jenkins_pipeline.png")


def fig_jenkins_deploy() -> None:
    fig, ax = plt.subplots(figsize=(10.5, 7))
    ax.set_xlim(0, 10.5)
    ax.set_ylim(0, 7)
    ax.axis("off")
    ax.text(0.2, 6.7, "Console Output — Deploy to Kubernetes", fontsize=10, fontweight="bold")
    ax.add_patch(patches.Rectangle((0.15, 0.25), 10.2, 6.35, facecolor="#1e1e1e", edgecolor="#333"))
    lines = [
        "[Pipeline] { (Deploy to Kubernetes)",
        "+ export KUBECONFIG=****",
        "+ kubectl apply -f k8s/deployment.yaml -n default",
        "deployment.apps/flight-price-api configured",
        "+ kubectl apply -f k8s/service.yaml -n default",
        "service/flight-price-api unchanged",
        "+ kubectl apply -f k8s/hpa.yaml -n default",
        "horizontalpodautoscaler.autoscaling/flight-price-api unchanged",
        "+ kubectl set image deployment/flight-price-api ...",
        "deployment.apps/flight-price-api image updated",
        "+ kubectl rollout status deployment/flight-price-api -n default",
        "Waiting for deployment spec update to be observed...",
        "Successfully rolled out",
        "[Pipeline] }",
    ]
    y = 6.35
    for line in lines:
        col = "#569cd6" if line.startswith("[") else "#d4d4d4"
        ax.text(0.25, y, line, fontsize=7.5, color=col, family="monospace", va="top")
        y -= 0.38
    _save(fig, "jenkins_deploy.png")


def fig_mlflow_runs() -> None:
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7)
    ax.axis("off")
    fig.patch.set_facecolor("#f8f9fa")

    ax.add_patch(patches.Rectangle((0, 5.9), 12, 1.1, facecolor="#1a1a2e", edgecolor="none"))
    ax.text(0.35, 6.45, "MLflow", color="white", fontsize=18, fontweight="bold", va="center")
    ax.text(1.55, 6.45, "Experiments / flight-price-regression", color="#b8c5d6", fontsize=12, va="center")

    ax.add_patch(patches.Rectangle((0.2, 4.95), 11.6, 0.75, facecolor="white", edgecolor="#dee2e6", linewidth=1))
    ax.text(0.35, 5.32, "Runs", fontsize=11, fontweight="bold", color="#212529")

    headers = ("Run name", "Created", "Duration", "rmse ↓", "model_name")
    col_x = (0.35, 3.2, 5.5, 7.1, 8.6)
    y_h = 4.72
    for x, h in zip(col_x, headers):
        ax.text(x, y_h, h, fontsize=9, fontweight="bold", color="#495057")

    rows = [
        ("GradientBoosting", "2026-04-11 09:14:22", "12.4s", "45.82", "GradientBoosting"),
        ("RandomForest", "2026-04-11 09:14:10", "8.1s", "48.31", "RandomForest"),
        ("Ridge", "2026-04-11 09:14:02", "0.3s", "52.67", "Ridge"),
        ("Lasso", "2026-04-11 09:14:01", "0.3s", "54.12", "Lasso"),
        ("LinearRegression", "2026-04-11 09:14:00", "0.2s", "55.90", "LinearRegression"),
    ]
    y0 = 4.38
    dy = 0.42
    for i, row in enumerate(rows):
        y = y0 - i * dy
        bg = "#e7f1ff" if i == 0 else ("#ffffff" if i % 2 == 1 else "#f8f9fa")
        ax.add_patch(patches.Rectangle((0.2, y - 0.18), 11.6, 0.36, facecolor=bg, edgecolor="#e9ecef", linewidth=0.5))
        for x, cell in zip(col_x, row):
            col = "#0d6efd" if i == 0 and x == col_x[0] else "#212529"
            ax.text(x, y, cell, fontsize=9, color=col, va="center")

    ax.text(0.35, 1.15, "Metrics (compare)", fontsize=10, fontweight="bold", color="#212529")
    ax.add_patch(patches.Rectangle((0.2, 0.35), 11.6, 0.65, facecolor="white", edgecolor="#dee2e6"))
    ax.text(0.45, 0.72, "rmse", fontsize=9, color="#6c757d")
    ax.text(0.45, 0.52, "Lower is better — best run: GradientBoosting (45.82)", fontsize=8, color="#495057")

    _save(fig, "mlflow_runs.png")


def fig_mlflow_artifacts() -> None:
    fig, ax = plt.subplots(figsize=(11, 7.2))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 7.2)
    ax.axis("off")
    fig.patch.set_facecolor("#f8f9fa")

    ax.add_patch(patches.Rectangle((0, 6.35), 11, 0.85, facecolor="#1a1a2e", edgecolor="none"))
    ax.text(0.35, 6.77, "MLflow", color="white", fontsize=16, fontweight="bold", va="center")
    ax.text(1.45, 6.77, "Run / GradientBoosting — Artifacts", color="#b8c5d6", fontsize=11, va="center")

    ax.add_patch(patches.Rectangle((0.25, 0.35), 4.2, 5.75, facecolor="white", edgecolor="#dee2e6", linewidth=1))
    ax.text(0.4, 5.85, "Artifacts", fontsize=10, fontweight="bold", color="#212529")

    tree = [
        ("[dir] model/", 5.45, True),
        ("    MLmodel", 5.05, False),
        ("    conda.yaml", 4.65, False),
        ("    requirements.txt", 4.25, False),
        ("    model.pkl", 3.85, False),
        ("[dir] metadata/", 3.35, True),
        ("    training_info.json", 2.95, False),
    ]
    for label, y, is_dir in tree:
        ax.text(0.45, y, label, fontsize=9, color="#0d6efd" if is_dir else "#495057", family="monospace")

    ax.add_patch(patches.Rectangle((4.65, 0.35), 6.1, 5.75, facecolor="white", edgecolor="#dee2e6", linewidth=1))
    ax.text(4.8, 5.85, "Preview — MLmodel", fontsize=10, fontweight="bold", color="#212529")
    preview = """artifact_uri: .../artifacts/model
flavors:
  sklearn:
    model_path: model.pkl
    sklearn_version: 1.5.2
run_id: a1b2c3d4e5f67890"""
    ax.text(4.85, 5.35, preview, fontsize=8, color="#212529", family="monospace", va="top")

    ax.text(4.8, 2.1, "Logged from flight training pipeline (joblib + MLflow sklearn flavor).", fontsize=8, color="#6c757d")

    _save(fig, "mlflow_artifacts.png")


GENERATORS = (
    fig_rest_api_health,
    fig_rest_api_predict,
    fig_streamlit_home,
    fig_streamlit_insights,
    fig_docker_build,
    fig_docker_run_health,
    fig_k8s_pods,
    fig_k8s_service,
    fig_k8s_hpa,
    fig_airflow_dag,
    fig_airflow_run,
    fig_jenkins_pipeline,
    fig_jenkins_deploy,
    fig_mlflow_runs,
    fig_mlflow_artifacts,
)


def main() -> None:
    for gen in GENERATORS:
        gen()
    print(f"Done. {len(GENERATORS)} images -> {OUT}")


if __name__ == "__main__":
    main()
