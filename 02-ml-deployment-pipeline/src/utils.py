import os, json
from datetime import datetime

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def timestamp():
    return datetime.utcnow().strftime("%Y%m%dT%H%M%S")

def save_metrics(artifact_dir, metrics: dict):
    with open(os.path.join(artifact_dir, "metrics.json"), "w") as f:
        json.dump(metrics, f, indent=2)

def save_info(artifact_dir, info: dict):
    with open(os.path.join(artifact_dir, "model_info.json"), "w") as f:
        json.dump(info, f, indent=2)
