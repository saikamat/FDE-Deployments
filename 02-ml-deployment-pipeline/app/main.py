from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np

from .model_loader import load_model

app = FastAPI(title="ML Deploy Pipeline - Inference API")

# Load model at startup
model, model_info = load_model()

class PredictRequest(BaseModel):
    features: list[float]

class PredictResponse(BaseModel):
    prediction: int
    class_name: str

@app.get("/")
def root():
    return {
        "message": "ML Inference API is running",
        "model": model_info.get("model_type"),
        "trained_on": model_info.get("created_utc"),
    }

@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    # Expect features as list[float], shape matches training data
    X = np.array(req.features).reshape(1, -1)
    pred = model.predict(X)[0]
    class_name = model_info["target_names"][pred]
    return {"prediction": int(pred), "class_name": class_name}

from mangum import Mangum
handler = Mangum(app)
