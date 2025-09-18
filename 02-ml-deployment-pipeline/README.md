# ML Deploy Pipeline

This repository is the starting point for building an end-to-end automated ML model deployment pipeline.
**The goal**: train a model, track experiments, version artifacts, and prepare for deployment on AWS (via Lambda, Docker, and Terraform), with CI/CD handled through GitHub Actions.

## Project Overview

This project demonstrates an end-to-end automated ML model deployment pipeline using modern DevOps practices. We're building a complete system that trains models, deploys them to AWS Lambda, and provides a scalable inference API.

## Architecture Components

- **Training Pipeline**: Scikit-learn RandomForest on Iris dataset with MLflow tracking -> - [01-Building Baseline Model](docs/01-Baseline-Model.md)
- **Inference Service**: FastAPI application with automatic model loading - [02-FastAPI-Inference-Service](docs/02-FastAPI-Inference-Service.md)
- **Containerization**: Docker containers optimized for AWS Lambda - [03-Dockerize](docs/03-Dockerize.md)
- **Cloud Deployment**: AWS Lambda with container images - [04-AWS Lambda with Container Images](docs/04-AWS-with-container-images.md)
- **API Gateway**: Public HTTPS endpoints for model predictions

## Current Progress Status

### ✅ Completed Steps

#### 1. Baseline Training Pipeline
- **Dataset**: Iris dataset (150 samples, 4 features, 3 classes)
- **Model**: RandomForest classifier with scikit-learn
- **Artifacts Saved**:
  - `model.joblib` → Serialized model
  - `metrics.json` → Accuracy, F1 scores, precision, recall
  - `model_info.json` → Metadata (features, timestamp, parameters, target names)
- **Tracking**: MLflow local file-based tracking (`mlruns/`)
- **Repository Structure**:
  ```
  ├── notebooks/          # Jupyter notebooks for experimentation
  ├── src/               # Training source code
  ├── artifacts/         # Model artifacts (auto-generated)
  ├── mlruns/           # MLflow tracking data
  └── docs/             # Documentation
  ```

#### 2. FastAPI Inference Service
- **Endpoints**:
  - `GET /` → Service status and model information
  - `POST /predict` → Model predictions with feature input
- **Model Loading**: Automatic loading of latest trained model
- **Input Validation**: Pydantic models for request/response validation
- **Local Testing**: Successfully tested with `uvicorn` and HTTP requests

#### 3. Docker Containerization
- **Base Image**: `public.ecr.aws/lambda/python:3.11` (AWS Lambda optimized)
- **Dependencies**: Pinned requirements with build tools for compilation
- **Optimization**: Multi-stage build with minimal final image size
- **Platform**: Built for `linux/amd64` (AWS Lambda compatible)
- **Handler**: Properly configured for Lambda runtime (`app.main.handler`)

#### 4. AWS Lambda Deployment
- **Container Registry**: Amazon ECR for image storage
- **Lambda Function**: Container-based deployment
- **Runtime**: Python 3.11 with custom container
- **Memory**: 512 MB (optimized for ML workloads)
- **Timeout**: 30 seconds (sufficient for model loading)
- **Testing**: Successfully tested with API Gateway proxy events

## Technical Implementation Details

### Training Pipeline (`src/train.py`)
```python
# Key features:
- MLflow experiment tracking
- Automatic artifact saving
- Model metadata generation
- Cross-validation metrics
- Confusion matrix visualization
```

### Inference Service (`app/main.py`)
```python
# Key features:
- FastAPI with automatic OpenAPI docs
- Mangum adapter for AWS Lambda
- Automatic model loading from artifacts
- Input validation with Pydantic
- Error handling and logging
```

### Model Loading (`app/model_loader.py`)
```python
# Key features:
- Automatic latest model detection
- Joblib model deserialization
- Metadata loading and validation
- Error handling for missing artifacts
```

### Docker Configuration
```dockerfile
# Key optimizations:
- AWS Lambda base image
- Build dependencies for Python packages
- Minimal final image size
- Proper working directory setup
- Lambda handler configuration
```

## Current Architecture Diagram

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Training      │    │   Model Storage   │    │   Inference     │
│   Pipeline      │───▶│   (Local Files)  │◀───│   Service       │
│                 │    │                  │    │                 │
│ • Jupyter       │    │ • model.joblib   │    │ • FastAPI       │
│ • MLflow        │    │ • metrics.json   │    │ • Mangum        │
│ • Scikit-learn  │    │ • model_info.json│    │ • Auto-loading  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                         │
                                                         ▼
                                               ┌─────────────────┐
                                               │   AWS Lambda     │
                                               │                 │
                                               │ • Container     │
                                               │ • ECR Image     │
                                               │ • Auto-scaling  │
                                               └─────────────────┘
                                                         │
                                                         ▼
                                               ┌─────────────────┐
                                               │   API Gateway    │
                                               │                 │
                                               │ • HTTPS Endpoint│
                                               │ • Rate Limiting │
                                               │ • Monitoring    │
                                               └─────────────────┘
```

## File Structure

```
02-ml-deployment-pipeline/
├── app/                    # FastAPI inference service
│   ├── main.py            # Main application with endpoints
│   ├── model_loader.py    # Model loading utilities
│   └── test_request.py    # Local testing script
├── artifacts/             # Model artifacts (auto-generated)
│   └── model_*/           # Timestamped model versions
├── docs/                  # Documentation
│   ├── README.md          # This file
│   ├── 01-Baseline-Model.md
│   ├── 02-FastAPI-Inference-Service.md
│   └── 02-Next-Steps.md
├── mlruns/               # MLflow tracking data
├── notebooks/            # Jupyter notebooks
│   └── 01-train.ipynb
├── src/                  # Training source code
│   ├── data_loader.py
│   ├── train.py
│   └── utils.py
├── Dockerfile            # Container configuration
├── requirements.txt     # Python dependencies
├── trust-policy.json    # AWS IAM trust policy
└── README.md            # Project overview
```


## Dependencies

### Training Environment
- Python 3.11+
- scikit-learn
- pandas
- numpy
- mlflow
- matplotlib
- jupyter

### Inference Environment
- Python 3.11+
- fastapi
- mangum
- numpy
- pandas
- scikit-learn
- joblib

## Performance Metrics

- **Model Accuracy**: ~97% on Iris dataset
- **Inference Latency**: <100ms (local)
- **Container Size**: ~500MB (optimized)
- **Cold Start Time**: ~3-5 seconds (Lambda)
- **Memory Usage**: ~50MB (inference)

---

*Last Updated: September 17, 2025*
*Status: Lambda deployment successful, ready for API Gateway integration*
# CI/CD Test
