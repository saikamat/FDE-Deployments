# What we’ll do in this step
1. Write a Dockerfile for the FastAPI app.
2. Add a .dockerignore to keep the image clean.
3. Build and run locally to confirm it works.
4. Test with curl or Python requests inside/outside the container.

We’ll keep this image generic enough so later we can push it to AWS ECR.

# Dockerized Inference Service

This step containerizes the FastAPI app so it can be deployed consistently across environments (local, AWS, CI/CD).

## Overview
- Uses a lightweight Python 3.11 slim base image.
- Installs required Python dependencies (scikit-learn, fastapi, uvicorn, joblib).
- Copies the `app/` code and `artifacts/` (latest model).
- Runs FastAPI with Uvicorn on port `8000`.

## Files
### [Dockerfile](../Dockerfile)
Defines the build process for the container image.
Key points:
- System deps installed (build-essential) for compiling ML libraries.
- Requirements installed first for better caching.
- Starts FastAPI with Uvicorn.
### [dockerignore](../.dockerignore)
Excludes unnecessary files from the image:
- Git metadata
- Jupyter notebooks
- Large/old model artifacts
- Logs, caches, etc.

## Building the image
From repo root folder
```bash
docker build -t ml-inference:latest .
```

## Running the Container
```bash
docker run -p 8000:8000 ml-inference:latest 
```
Output
```bash
INFO:     Started server process [1]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     192.168.65.1:54914 - "GET / HTTP/1.1" 200 OK
```

## Testing
Run the following command in CLI:-
```curl
curl -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"features":[5.1, 3.5, 1.4, 0.2]}'
```

Expected Output
```json
{
  "prediction": 0,
  "class_name": "setosa"
}
```