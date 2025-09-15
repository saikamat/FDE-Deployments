# Authentication Documentation

## Overview
The application uses AWS IAM-based authentication to access Amazon Bedrock services. There is no user authentication system implemented - the chatbot is designed as a public interface that authenticates with AWS services using stored credentials.

## Authentication Architecture

### AWS Authentication Flow
```
Application → AWS Credentials → IAM Authentication → Bedrock Service Access
```

### Authentication Methods

#### 1. Environment Variable Authentication
- **Method**: AWS Access Key ID and Secret Access Key
- **Storage**: Environment variables loaded from `.env` file
- **Implementation**:
  ```python
  aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
  aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
  aws_region = os.getenv("AWS_REGION", "eu-central-1")
  ```

#### 2. AWS Client Configuration
- **Service**: Amazon Bedrock Runtime
- **Region**: Configurable (default: eu-central-1)
- **Retry Configuration**: Adaptive retry with exponential backoff

## Credential Management

### Environment Variables Required
```bash
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here
AWS_REGION=eu-central-1
```

### Security Best Practices

#### 1. Credential Storage
- **Never commit credentials to version control**
- **Use environment variables for sensitive data**
- **Implement `.gitignore` to exclude credential files**
- **Consider using AWS IAM roles for production**

#### 2. Access Control
- **Principle of least privilege**: Only grant necessary permissions
- **Regular credential rotation**: Update access keys periodically
- **Monitor access logs**: Use AWS CloudTrail for audit trails

#### 3. Production Considerations
- **Use IAM roles instead of access keys when possible**
- **Implement temporary credentials for enhanced security**
- **Use AWS Secrets Manager for credential storage**

## AWS Permissions Required

### Minimum Required Permissions
The AWS user/role needs the following permissions for Amazon Bedrock:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel"
            ],
            "Resource": [
                "arn:aws:bedrock:*:*:model/anthropic.claude-3-sonnet-20240229-v1:0"
            ]
        }
    ]
}
```

### Additional Recommended Permissions
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel",
                "bedrock:ListFoundationModels"
            ],
            "Resource": "*"
        }
    ]
}
```

## Error Handling

### Authentication Errors
- **InvalidCredentials**: Check AWS access keys and secret keys
- **AccessDenied**: Verify IAM permissions for Bedrock access
- **RegionNotSupported**: Ensure Claude model is available in the specified region

### Error Recovery
```python
try:
    response = bedrock_client.invoke_model(...)
except ClientError as e:
    error_code = e.response['Error']['Code']
    if error_code == 'AccessDenied':
        # Handle authentication/permission errors
    elif error_code == 'InvalidParameterException':
        # Handle configuration errors
```

## Session Management

### No User Sessions
- **Public Access**: No user authentication required
- **Stateless Design**: Each request is independent
- **Session State**: Only maintains chat history in memory

### Streamlit Session State
- **Chat History**: Stored in `st.session_state.messages`
- **Temporary Storage**: Data lost on page refresh
- **No Persistence**: No database or file storage

## Security Considerations

### Data Protection
- **No User Data Storage**: Conversations not persisted
- **Memory-Only Storage**: Chat history exists only in session
- **No Personal Information**: No user registration or data collection

### Network Security
- **HTTPS Communication**: All AWS API calls use secure connections
- **No Direct Database Access**: Application doesn't connect to databases
- **API-Only Architecture**: All external communication through AWS APIs

### Vulnerability Mitigation
- **Input Validation**: Streamlit handles basic input sanitization
- **Error Information**: Limited error details exposed to users
- **Rate Limiting**: Built-in throttling protection

## Development vs Production

### Development Environment
- **Local Credentials**: Use personal AWS access keys
- **Environment Files**: Store credentials in `.env` files
- **Direct API Access**: Connect directly to AWS services

### Production Environment
- **IAM Roles**: Use AWS IAM roles instead of access keys
- **Container Deployment**: Deploy in containers with role-based access
- **Secrets Management**: Use AWS Secrets Manager or similar
- **Monitoring**: Implement CloudWatch logging and monitoring

## Troubleshooting Authentication Issues

### Common Problems

#### 1. Credential Not Found
```bash
# Check if environment variables are loaded
echo $AWS_ACCESS_KEY_ID
echo $AWS_SECRET_ACCESS_KEY
```

#### 2. Invalid Credentials
- Verify access key and secret key are correct
- Check if credentials have expired
- Ensure credentials have necessary permissions

#### 3. Region Issues
- Confirm Claude model is available in the specified region
- Check AWS region configuration
- Verify model ID is correct for the region

#### 4. Permission Denied
- Review IAM policy for Bedrock permissions
- Ensure user/role has `bedrock:InvokeModel` permission
- Check resource ARN restrictions

### Debug Steps
1. **Verify Environment Variables**: Check if credentials are loaded
2. **Test AWS CLI**: Use AWS CLI to test credentials
3. **Check IAM Permissions**: Review user/role permissions
4. **Validate Region**: Ensure Claude is available in the region
5. **Review Logs**: Check application logs for specific error messages

## Future Enhancements

### Potential Improvements
- **Multi-tenant Support**: Implement user authentication for multiple users
- **Role-based Access**: Different permission levels for different users
- **OAuth Integration**: Support for third-party authentication providers
- **Session Persistence**: Store chat history in secure database
- **Audit Logging**: Track user interactions and API usage
