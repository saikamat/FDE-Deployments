# GitHub Actions CI/CD Pipeline

## Overview

This document describes the automated CI/CD pipeline built with GitHub Actions that automates the entire ML deployment process from code changes to production deployment.

## Pipeline Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Code Push     │───▶│   GitHub        │───▶│   AWS           │
│   (main branch) │    │   Actions       │    │   Deployment    │
│                 │    │                 │    │                 │
│ • Pull Request  │    │ • Run Tests     │    │ • Build Image   │
│ • Direct Push   │    │ • Build Docker  │    │ • Push to ECR   │
│ • Tag Release   │    │ • Deploy Lambda │    │ • Update Lambda │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Pipeline Workflow

### Trigger Events
- **Push to main branch**: Full build and deployment
- **Pull Request**: Testing only (no deployment)

### Workflow Steps

#### 1. Test Job
- **Runs on**: `ubuntu-latest`
- **Triggers**: All pushes and pull requests
- **Steps**:
  1. Checkout code
  2. Set up Python 3.11
  3. Install dependencies
  4. Run validation tests
  5. Test model loading

#### 2. Build and Deploy Job
- **Runs on**: `ubuntu-latest`
- **Triggers**: Only on main branch pushes
- **Dependencies**: Requires test job to pass
- **Steps**:
  1. Checkout code
  2. Configure AWS credentials
  3. Login to Amazon ECR
  4. Build Docker image
  5. Push image to ECR
  6. Update Lambda function
  7. Test deployment
  8. Create deployment summary

## Setup Instructions

### Step 1: Create AWS IAM User

1. **Go to AWS IAM Console**
   - Navigate to IAM → Users → Create user

2. **User Details**
   - **User name**: `github-actions-ml-pipeline`
   - **Access type**: Programmatic access

3. **Attach Policy**
   - Use the policy from `github-actions-policy.json`
   - Or attach these managed policies:
     - `AmazonEC2ContainerRegistryFullAccess`
     - `AWSLambdaFullAccess`

4. **Create Access Keys**
   - Download the access key ID and secret access key
   - **Important**: Save these securely - you won't see the secret again

### Step 2: Configure GitHub Secrets

1. **Go to GitHub Repository**
   - Navigate to your repo → Settings → Secrets and variables → Actions

2. **Add Repository Secrets**:
   ```
   AWS_ACCESS_KEY_ID: AKIA...
   AWS_SECRET_ACCESS_KEY: your-secret-key
   API_GATEWAY_URL: https://kx1yg8qvj2.execute-api.eu-central-1.amazonaws.com/prod
   ```

### Step 3: Update Workflow Configuration

Edit `.github/workflows/deploy.yml` and update these values:

```yaml
env:
  AWS_REGION: eu-central-1  # Change to your region
  ECR_REPOSITORY: ml-inference  # Change to your ECR repo name
  LAMBDA_FUNCTION_NAME: ml-inference-function  # Change to your Lambda name
```

### Step 4: Test the Pipeline

1. **Create a test branch**:
   ```bash
   git checkout -b test-ci-cd
   git push origin test-ci-cd
   ```

2. **Create a Pull Request**:
   - This will trigger the test job only
   - Verify tests pass

3. **Merge to main**:
   - This will trigger the full deployment pipeline
   - Monitor the Actions tab for progress

## Workflow File Structure

```
.github/
└── workflows/
    └── deploy.yml          # Main CI/CD workflow

tests/
└── test_app.py            # Unit tests for the application

github-actions-policy.json  # IAM policy for GitHub Actions
```

## Key Features

### Automated Testing
- **Unit Tests**: FastAPI endpoint testing
- **Model Validation**: Ensures model loads correctly
- **Input Validation**: Tests error handling
- **Integration Tests**: End-to-end API testing

### Docker Build Process
- **Multi-platform**: Built for `linux/amd64` (AWS Lambda compatible)
- **Optimized**: Uses `--provenance=false` for faster builds
- **Tagged**: Uses Git commit SHA for unique image tags
- **Cached**: Leverages Docker layer caching

### AWS Deployment
- **ECR Integration**: Automatic login and push
- **Lambda Update**: Seamless function code updates
- **Health Checks**: Post-deployment testing
- **Rollback Ready**: Previous versions remain available

### Monitoring and Feedback
- **Deployment Summary**: GitHub Actions summary with links
- **Test Results**: Detailed test output
- **Error Handling**: Clear error messages and debugging info

## Testing Strategy

### Local Testing
```bash
# Run tests locally
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=app --cov-report=html
```

### CI Testing
- **Automated**: Runs on every push and PR
- **Comprehensive**: Tests all endpoints and error cases
- **Fast**: Optimized for quick feedback
- **Reliable**: Uses pinned dependency versions

### Deployment Testing
- **Health Checks**: Tests both endpoints after deployment
- **Smoke Tests**: Basic functionality verification
- **Integration**: Tests the full API Gateway → Lambda flow

## Security Considerations

### AWS Credentials
- **Least Privilege**: Minimal required permissions
- **Secrets Management**: Stored securely in GitHub Secrets
- **Rotation**: Regular credential rotation recommended

### IAM Policy Scope
```json
{
  "Effect": "Allow",
  "Action": [
    "ecr:*",           // ECR operations
    "lambda:UpdateFunctionCode",  // Lambda updates
    "lambda:GetFunction",        // Lambda read access
    "logs:*"           // CloudWatch logs
  ],
  "Resource": "specific-arns"  // Scoped to specific resources
}
```

### Network Security
- **HTTPS Only**: All API Gateway endpoints use HTTPS
- **Regional**: Resources deployed in specific AWS region
- **VPC**: Can be extended to VPC for additional security

## Troubleshooting

### Common Issues

#### 1. AWS Credentials Error
**Problem**: `The security token included in the request is invalid`

**Solutions**:
- Verify AWS credentials in GitHub Secrets
- Check IAM user has correct permissions
- Ensure region matches your resources

#### 2. ECR Login Failed
**Problem**: `Unable to locate credentials`

**Solutions**:
- Verify ECR repository exists
- Check AWS region configuration
- Ensure IAM user has ECR permissions

#### 3. Lambda Update Failed
**Problem**: `Function not found` or `Access denied`

**Solutions**:
- Verify Lambda function name in workflow
- Check IAM permissions for Lambda
- Ensure function exists in correct region

#### 4. Tests Failing
**Problem**: Tests fail in CI but pass locally

**Solutions**:
- Check Python version compatibility
- Verify all dependencies are in requirements.txt
- Ensure test data is available in CI environment

### Debugging Steps

1. **Check GitHub Actions Logs**:
   - Go to Actions tab → Select workflow run
   - Expand failed step for detailed logs

2. **Test Locally**:
   ```bash
   # Test Docker build
   docker build --platform linux/amd64 -t test-image .
   
   # Test AWS CLI
   aws sts get-caller-identity
   aws ecr describe-repositories
   ```

3. **Verify AWS Resources**:
   - Check ECR repository exists
   - Verify Lambda function name
   - Confirm API Gateway URL

## Performance Optimization

### Build Optimization
- **Docker Caching**: Leverages layer caching
- **Parallel Jobs**: Test and build can run in parallel
- **Minimal Dependencies**: Only install required packages

### Deployment Optimization
- **Incremental Updates**: Only updates changed code
- **Health Checks**: Quick validation after deployment
- **Rollback**: Previous versions remain available

### Cost Optimization
- **On-demand**: Only runs when needed
- **Efficient**: Minimal compute time
- **Cached**: Reuses Docker layers

## Monitoring and Alerts

### GitHub Actions
- **Status Badges**: Add to README for build status
- **Notifications**: Email/Slack notifications for failures
- **Retention**: Automatic log retention

### AWS CloudWatch
- **Lambda Metrics**: Function execution metrics
- **API Gateway**: Request/response metrics
- **Alarms**: Set up alerts for errors

## Future Enhancements

### Advanced Features
- **Multi-environment**: Dev/staging/production pipelines
- **Blue/Green Deployments**: Zero-downtime deployments
- **Canary Releases**: Gradual rollout of changes
- **Automated Rollbacks**: Automatic rollback on failures

### Security Improvements
- **VPC Integration**: Deploy Lambda in VPC
- **API Keys**: Add API key authentication
- **WAF**: Web Application Firewall protection
- **Secrets Rotation**: Automated credential rotation

### Monitoring Enhancements
- **Distributed Tracing**: End-to-end request tracing
- **Custom Metrics**: Business-specific metrics
- **Dashboards**: Real-time monitoring dashboards
- **Alerting**: Advanced alerting rules

---

*Last Updated: September 17, 2025*
*Status: CI/CD pipeline implemented and operational*
