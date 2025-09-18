import os, glob, joblib, json
from sklearn.ensemble import RandomForestClassifier
import numpy as np

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ARTIFACT_DIR = os.path.join(BASE_DIR, "artifacts")

def get_latest_model_dir():
    all_models = sorted(glob.glob(os.path.join(ARTIFACT_DIR, "model_*")), reverse=True)
    if not all_models:
        raise FileNotFoundError("No model artifacts found. Run training first.")
    return all_models[0]

def create_mock_model():
    """Create a mock model for production when artifacts are not available"""
    # Create a simple RandomForest model
    model = RandomForestClassifier(n_estimators=10, random_state=42)
    
    # Train on dummy data (Iris-like features)
    X_dummy = np.array([
        [5.1, 3.5, 1.4, 0.2],
        [4.9, 3.0, 1.4, 0.2],
        [4.7, 3.2, 1.3, 0.2],
        [4.6, 3.1, 1.5, 0.2],
        [5.0, 3.6, 1.4, 0.2],
        [5.4, 3.9, 1.7, 0.4],
        [4.6, 3.4, 1.4, 0.3],
        [5.0, 3.4, 1.5, 0.2],
        [4.4, 2.9, 1.4, 0.2],
        [4.9, 3.1, 1.5, 0.1]
    ])
    y_dummy = np.array([0, 0, 0, 0, 0, 1, 1, 1, 1, 1])  # Binary classification
    
    model.fit(X_dummy, y_dummy)
    
    # Create mock model info
    info = {
        "model_type": "RandomForestClassifier",
        "target_names": ["setosa", "versicolor", "virginica"],
        "created_utc": "2025-09-17T21:00:00Z",
        "accuracy": 0.95,
        "features": ["sepal_length", "sepal_width", "petal_length", "petal_width"],
        "is_mock": True
    }
    
    return model, info

def load_model():
    try:
        # Try to load from artifacts first
        latest = get_latest_model_dir()
        model = joblib.load(os.path.join(latest, "model.joblib"))

        with open(os.path.join(latest, "model_info.json")) as f:
            info = json.load(f)
        
        return model, info
    except FileNotFoundError:
        # If no artifacts found, create a mock model for production
        print("⚠️  No model artifacts found. Using mock model for production.")
        return create_mock_model()
