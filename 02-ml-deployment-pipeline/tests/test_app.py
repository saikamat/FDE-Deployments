import pytest
import json
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root_endpoint():
    """Test the root endpoint returns correct response"""
    response = client.get("/")
    assert response.status_code == 200
    
    data = response.json()
    assert "message" in data
    assert "model" in data
    assert "trained_on" in data
    assert data["message"] == "ML Inference API is running"

def test_predict_endpoint():
    """Test the predict endpoint with valid input"""
    test_data = {
        "features": [5.1, 3.5, 1.4, 0.2]
    }
    
    response = client.post("/predict", json=test_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "prediction" in data
    assert "class_name" in data
    assert isinstance(data["prediction"], int)
    assert isinstance(data["class_name"], str)

def test_predict_endpoint_invalid_input():
    """Test the predict endpoint with invalid input"""
    # Test with wrong number of features
    test_data = {
        "features": [5.1, 3.5]  # Only 2 features instead of 4
    }
    
    response = client.post("/predict", json=test_data)
    assert response.status_code == 422  # Validation error

def test_predict_endpoint_missing_features():
    """Test the predict endpoint with missing features"""
    test_data = {}  # No features field
    
    response = client.post("/predict", json=test_data)
    assert response.status_code == 422  # Validation error

def test_model_loading():
    """Test that model can be loaded successfully"""
    from app.model_loader import load_model
    
    model, model_info = load_model()
    
    # Check model is loaded
    assert model is not None
    assert model_info is not None
    
    # Check model info has required fields
    assert "model_type" in model_info
    assert "target_names" in model_info
    assert "created_utc" in model_info
    
    # Check target names
    assert len(model_info["target_names"]) == 3  # Iris has 3 classes
    assert "setosa" in model_info["target_names"]
    assert "versicolor" in model_info["target_names"]
    assert "virginica" in model_info["target_names"]
