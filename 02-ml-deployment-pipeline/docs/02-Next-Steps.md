Roadmap (Next Steps)
Step 1: Inference API

Wrap the trained model.joblib in a simple FastAPI service (predict endpoint).

Test it locally (no Docker yet).

Step 2: Dockerize

Create Dockerfile + docker-compose.yml.

Containerize the FastAPI service with the model artifact.

Run/test locally (curl or Postman).

Step 3: AWS Lambda (Container Image)

Push Docker image to AWS ECR.

Deploy as AWS Lambda function (container-based, not zip).

Wire it up to API Gateway for HTTPS endpoint.

Step 4: Infrastructure as Code (Terraform)

Define infra for:

ECR repo

Lambda function

API Gateway

S3 bucket (to hold future new training data)

EventBridge rule (trigger retraining when new data arrives)

Step 5: CI/CD (GitHub Actions)

Add workflows:

CI: run tests + training on pushes

CD: build Docker, push to ECR, deploy via Terraform

Step 6: Retraining Automation

Watch S3 for new data.

Trigger retrain job (via CodeBuild or Lambda).

Register new model → update Lambda → redeploy.