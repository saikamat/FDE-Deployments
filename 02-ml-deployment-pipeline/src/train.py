import os, json
from datetime import datetime
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score

from .data_loader import load_iris
from .utils import ensure_dir, save_metrics, save_info

try:
    import mlflow, mlflow.sklearn
    MLFLOW = True
except:
    MLFLOW = False

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ART_DIR = os.path.join(BASE_DIR, "artifacts")
ensure_dir(ART_DIR)

def train(n_estimators=300, max_depth=None, experiment="baseline-iris"):
    (X_train, y_train), (X_test, y_test), feature_names, target_names = load_iris()
    model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, n_jobs=-1, random_state=42)

    if MLFLOW:
        mlflow.set_tracking_uri(f"file://{os.path.join(BASE_DIR, 'mlruns')}")
        mlflow.set_experiment(experiment)
        with mlflow.start_run() as run:
            model.fit(X_train, y_train)
            preds = model.predict(X_test)
            acc = accuracy_score(y_test, preds)
            f1 = f1_score(y_test, preds, average="macro")

            mlflow.log_param("n_estimators", n_estimators)
            mlflow.log_param("max_depth", max_depth)
            mlflow.log_metric("accuracy", acc)
            mlflow.log_metric("f1_macro", f1)

            stamp = datetime.utcnow().strftime("%Y%m%dT%H%M%S")
            out = os.path.join(ART_DIR, f"model_{stamp}")
            ensure_dir(out)
            joblib.dump(model, os.path.join(out, "model.joblib"))

            save_metrics(out, {"accuracy": acc, "f1_macro": f1})
            save_info(out, {
                "model_type": "RandomForestClassifier",
                "n_estimators": n_estimators,
                "max_depth": max_depth,
                "feature_names": feature_names,
                "target_names": target_names.tolist(),
                "created_utc": datetime.utcnow().isoformat() + "Z",
                "mlflow_run_id": run.info.run_id
            })

            mlflow.log_artifacts(out, artifact_path="model_artifacts")
            mlflow.sklearn.log_model(model, "sk_model")

            print("Saved:", out)
            print("Run ID:", run.info.run_id)
            return out
    else:
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        acc = accuracy_score(y_test, preds)
        f1 = f1_score(y_test, preds, average="macro")

        stamp = datetime.utcnow().strftime("%Y%m%dT%H%M%S")
        out = os.path.join(ART_DIR, f"model_{stamp}")
        ensure_dir(out)
        joblib.dump(model, os.path.join(out, "model.joblib"))
        save_metrics(out, {"accuracy": acc, "f1_macro": f1})
        save_info(out, {
            "model_type": "RandomForestClassifier",
            "n_estimators": n_estimators,
            "max_depth": max_depth,
            "feature_names": feature_names,
            "target_names": target_names.tolist(),
            "created_utc": datetime.utcnow().isoformat() + "Z",
        })
        print("Saved:", out)
        return out

if __name__ == "__main__":
    train()