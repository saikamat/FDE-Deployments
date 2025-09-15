import os, glob, joblib, json

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ARTIFACT_DIR = os.path.join(BASE_DIR, "artifacts")

def get_latest_model_dir():
    all_models = sorted(glob.glob(os.path.join(ARTIFACT_DIR, "model_*")), reverse=True)
    if not all_models:
        raise FileNotFoundError("No model artifacts found. Run training first.")
    return all_models[0]

def load_model():
    latest = get_latest_model_dir()
    model = joblib.load(os.path.join(latest, "model.joblib"))

    with open(os.path.join(latest, "model_info.json")) as f:
        info = json.load(f)

    return model, info
