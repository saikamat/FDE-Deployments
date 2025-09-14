# Environmental Variables Documentation

## Overview
The application uses environment variables for configuration management, particularly for AWS credentials and service settings. This approach provides security, flexibility, and separation of configuration from code.

## Environment Variable Structure

### 1. AWS Credentials
```bash
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here
AWS_REGION=eu-central-1
```

### 2. Current Implementation
The application currently uses a `.env` file approach with the following structure:

#### Environment File (.env)
```bash
# AWS Configuration
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here
AWS_REGION=eu-central-1
```

#### OpenAI Environment File (openai_env.env)
```bash
# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here
```

## Environment Variable Usage

### 1. Loading Environment Variables
```python
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
```

### 2. Retrieving Environment Variables
```python
# AWS credentials
aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
aws_region = os.getenv("AWS_REGION", "eu-central-1")  # Default value
```

### 3. Default Values
```python
# Provide default values for optional variables
aws_region = os.getenv("AWS_REGION", "eu-central-1")
```

## Configuration Management

### 1. Environment File Structure
```
project-root/
├── .env                    # Main environment file
├── openai_env.env         # OpenAI-specific configuration
├── .gitignore             # Excludes .env files from version control
└── app.py                 # Application code
```

### 2. Environment File Loading
```python
# Load multiple environment files if needed
load_dotenv()  # Loads .env by default
load_dotenv("openai_env.env")  # Load additional env file
```

### 3. Environment Variable Validation
```python
# Check if required variables are set
required_vars = ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"]
missing_vars = [var for var in required_vars if not os.getenv(var)]

if missing_vars:
    raise ValueError(f"Missing required environment variables: {missing_vars}")
```

## Security Considerations

### 1. Credential Protection
- **Never commit .env files to version control**
- **Use .gitignore to exclude sensitive files**
- **Store credentials securely in production environments**

### 2. Environment File Security
```bash
# .gitignore should include:
.env
*.env
openai_env.env
```

### 3. Production Security
- **Use IAM roles instead of access keys when possible**
- **Implement secrets management (AWS Secrets Manager, etc.)**
- **Rotate credentials regularly**
- **Monitor credential usage**

## Environment-Specific Configuration

### 1. Development Environment
```bash
# .env (development)
AWS_ACCESS_KEY_ID=dev_access_key
AWS_SECRET_ACCESS_KEY=dev_secret_key
AWS_REGION=us-east-1
```

### 2. Production Environment
```bash
# Production environment variables
AWS_ACCESS_KEY_ID=prod_access_key
AWS_SECRET_ACCESS_KEY=prod_secret_key
AWS_REGION=eu-central-1
```

### 3. Testing Environment
```bash
# .env.test
AWS_ACCESS_KEY_ID=test_access_key
AWS_SECRET_ACCESS_KEY=test_secret_key
AWS_REGION=us-west-2
```

## Environment Variable Types

### 1. Required Variables
- **AWS_ACCESS_KEY_ID**: AWS access key for authentication
- **AWS_SECRET_ACCESS_KEY**: AWS secret key for authentication

### 2. Optional Variables
- **AWS_REGION**: AWS region (default: eu-central-1)
- **OPENAI_API_KEY**: OpenAI API key (currently unused)

### 3. Future Variables
- **LOG_LEVEL**: Application logging level
- **MAX_TOKENS**: Maximum tokens for Claude responses
- **TEMPERATURE**: Claude model temperature setting
- **TOP_P**: Claude model top_p setting

## Environment Variable Validation

### 1. Basic Validation
```python
def validate_environment():
    """Validate required environment variables"""
    required_vars = {
        "AWS_ACCESS_KEY_ID": "AWS Access Key ID",
        "AWS_SECRET_ACCESS_KEY": "AWS Secret Access Key"
    }
    
    missing_vars = []
    for var, description in required_vars.items():
        if not os.getenv(var):
            missing_vars.append(f"{var} ({description})")
    
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
    
    return True
```

### 2. Advanced Validation
```python
def validate_aws_credentials():
    """Validate AWS credentials format"""
    access_key = os.getenv("AWS_ACCESS_KEY_ID")
    secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    
    if access_key and len(access_key) != 20:
        raise ValueError("AWS_ACCESS_KEY_ID must be 20 characters long")
    
    if secret_key and len(secret_key) != 40:
        raise ValueError("AWS_SECRET_ACCESS_KEY must be 40 characters long")
    
    return True
```

## Environment Variable Management

### 1. Development Setup
```bash
# Create .env file
cp .env.example .env

# Edit with your credentials
nano .env
```

### 2. Production Deployment
```bash
# Set environment variables in production
export AWS_ACCESS_KEY_ID="your_production_key"
export AWS_SECRET_ACCESS_KEY="your_production_secret"
export AWS_REGION="eu-central-1"
```

### 3. Docker Environment
```dockerfile
# Dockerfile
FROM python:3.9-slim

# Copy environment file
COPY .env /app/.env

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application
COPY app.py .

# Run application
CMD ["streamlit", "run", "app.py"]
```

## Environment Variable Best Practices

### 1. Naming Conventions
- **Use UPPERCASE**: Environment variable names should be uppercase
- **Use underscores**: Separate words with underscores
- **Be descriptive**: Use clear, descriptive names
- **Prefix appropriately**: Use service prefixes (AWS_, OPENAI_, etc.)

### 2. Default Values
```python
# Provide sensible defaults
aws_region = os.getenv("AWS_REGION", "eu-central-1")
max_tokens = int(os.getenv("MAX_TOKENS", "1000"))
temperature = float(os.getenv("TEMPERATURE", "0.7"))
```

### 3. Type Conversion
```python
# Convert string environment variables to appropriate types
max_tokens = int(os.getenv("MAX_TOKENS", "1000"))
temperature = float(os.getenv("TEMPERATURE", "0.7"))
debug_mode = os.getenv("DEBUG", "false").lower() == "true"
```

## Environment Variable Documentation

### 1. Required Variables
| Variable | Description | Example | Required |
|----------|-------------|---------|----------|
| AWS_ACCESS_KEY_ID | AWS access key for authentication | AKIAIOSFODNN7EXAMPLE | Yes |
| AWS_SECRET_ACCESS_KEY | AWS secret key for authentication | wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY | Yes |

### 2. Optional Variables
| Variable | Description | Example | Default |
|----------|-------------|---------|---------|
| AWS_REGION | AWS region for Bedrock service | eu-central-1 | eu-central-1 |
| OPENAI_API_KEY | OpenAI API key | sk-... | None |

### 3. Future Variables
| Variable | Description | Example | Default |
|----------|-------------|---------|---------|
| MAX_TOKENS | Maximum tokens for Claude responses | 1000 | 1000 |
| TEMPERATURE | Claude model temperature | 0.7 | 0.7 |
| TOP_P | Claude model top_p setting | 0.9 | 0.9 |
| LOG_LEVEL | Application logging level | INFO | INFO |

## Troubleshooting Environment Variables

### 1. Common Issues
- **Missing .env file**: Create .env file with required variables
- **Incorrect variable names**: Check spelling and case sensitivity
- **Missing values**: Ensure all required variables have values
- **File permissions**: Check .env file permissions

### 2. Debug Environment Variables
```python
def debug_environment():
    """Debug environment variable loading"""
    print("Environment Variables:")
    print(f"AWS_ACCESS_KEY_ID: {'SET' if os.getenv('AWS_ACCESS_KEY_ID') else 'NOT SET'}")
    print(f"AWS_SECRET_ACCESS_KEY: {'SET' if os.getenv('AWS_SECRET_ACCESS_KEY') else 'NOT SET'}")
    print(f"AWS_REGION: {os.getenv('AWS_REGION', 'NOT SET')}")
    print(f"OPENAI_API_KEY: {'SET' if os.getenv('OPENAI_API_KEY') else 'NOT SET'}")
```

### 3. Environment Variable Testing
```python
def test_environment():
    """Test environment variable configuration"""
    try:
        validate_environment()
        validate_aws_credentials()
        print("Environment configuration is valid")
        return True
    except Exception as e:
        print(f"Environment configuration error: {e}")
        return False
```

## Future Enhancements

### 1. Enhanced Configuration
- **Configuration classes**: Use Pydantic for configuration validation
- **Multiple environments**: Support for dev, staging, production configs
- **Secrets management**: Integration with AWS Secrets Manager
- **Configuration validation**: Enhanced validation and error handling

### 2. Environment Management
- **Environment switching**: Easy switching between environments
- **Configuration templates**: Template-based configuration
- **Dynamic configuration**: Runtime configuration updates
- **Configuration monitoring**: Monitor configuration changes

### 3. Security Improvements
- **Encrypted storage**: Encrypt sensitive environment variables
- **Access control**: Implement access control for configuration
- **Audit logging**: Log configuration access and changes
- **Compliance**: Ensure compliance with security standards
