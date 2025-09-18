import pytest
import os
from unittest.mock import patch, MagicMock

def test_model_loader_imports():
    """Test that model loader can be imported without errors"""
    from app.model_loader import get_latest_model_dir, load_model
    assert callable(get_latest_model_dir)
    assert callable(load_model)

def test_model_loader_handles_missing_artifacts():
    """Test that model loader handles missing artifacts gracefully"""
    from app.model_loader import get_latest_model_dir
    
    # This should raise FileNotFoundError when no artifacts exist
    with pytest.raises(FileNotFoundError, match="No model artifacts found"):
        get_latest_model_dir()

def test_fastapi_components():
    """Test that FastAPI components can be imported"""
    from fastapi import FastAPI
    from pydantic import BaseModel
    import numpy as np
    
    # Test creating FastAPI app
    app = FastAPI(title="Test App")
    assert app is not None
    
    # Test creating Pydantic models
    class TestRequest(BaseModel):
        features: list[float]
    
    class TestResponse(BaseModel):
        prediction: int
        class_name: str
    
    # Test model validation
    request = TestRequest(features=[1.0, 2.0, 3.0, 4.0])
    assert request.features == [1.0, 2.0, 3.0, 4.0]
    
    response = TestResponse(prediction=0, class_name="test")
    assert response.prediction == 0
    assert response.class_name == "test"

def test_dependencies_available():
    """Test that all required dependencies are available"""
    import joblib
    import json
    import numpy as np
    import pandas as pd
    import fastapi
    import mangum
    import sklearn
    from sklearn.ensemble import RandomForestClassifier
    
    # Test basic functionality
    assert hasattr(np, 'array')
    assert hasattr(pd, 'DataFrame')
    assert RandomForestClassifier is not None
    assert hasattr(sklearn, 'ensemble')

@patch('app.model_loader.load_model')
def test_app_with_mock_model(mock_load_model):
    """Test app functionality with mocked model"""
    # Mock the model loading
    mock_model = MagicMock()
    mock_model.predict.return_value = [0]
    mock_info = {
        "model_type": "RandomForestClassifier",
        "target_names": ["setosa", "versicolor", "virginica"],
        "created_utc": "2025-09-15T20:03:52Z"
    }
    mock_load_model.return_value = (mock_model, mock_info)
    
    # Now we can import the main app
    from app.main import app, PredictRequest, PredictResponse
    
    # Test that the app was created
    assert app is not None
    assert app.title == "ML Deploy Pipeline - Inference API"
    
    # Test request/response models
    request = PredictRequest(features=[5.1, 3.5, 1.4, 0.2])
    assert request.features == [5.1, 3.5, 1.4, 0.2]
    
    response = PredictResponse(prediction=0, class_name="setosa")
    assert response.prediction == 0
    assert response.class_name == "setosa"
