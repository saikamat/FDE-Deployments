# Architecture Documentation

## Overview
This is a Streamlit-based chatbot application that integrates with Amazon Bedrock's Claude Sonnet model to provide conversational AI capabilities. The architecture follows a simple but robust client-server pattern with AWS cloud integration.

## System Architecture

### High-Level Architecture
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   User Browser  │◄──►│  Streamlit App   │◄──►│  AWS Bedrock    │
│                 │    │   (Frontend +    │    │   Claude API    │
│                 │    │    Backend)      │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

### Component Architecture

#### 1. Frontend Layer (Streamlit UI)
- **Technology**: Streamlit web framework
- **Purpose**: Provides the user interface for chat interactions
- **Components**:
  - Chat interface with message history
  - Input field for user queries
  - Real-time message display
  - Loading states and error handling

#### 2. Application Layer (Python Backend)
- **Technology**: Python with Streamlit
- **Purpose**: Handles business logic, state management, and API integration
- **Key Functions**:
  - `main()`: Application entry point and UI orchestration
  - `call_claude_model()`: Core AI interaction logic
  - `get_bedrock_client()`: AWS client configuration

#### 3. Cloud Integration Layer
- **Technology**: AWS Bedrock Runtime API
- **Purpose**: Provides access to Claude Sonnet model
- **Features**:
  - Retry logic with exponential backoff
  - Rate limiting handling
  - Error management and recovery

## Design Patterns

### 1. Session State Management
- Uses Streamlit's built-in session state for maintaining chat history
- Implements persistent conversation context across user interactions

### 2. Retry Pattern
- Implements exponential backoff for handling AWS API rate limits
- Configurable retry attempts with adaptive delays
- Graceful degradation on persistent failures

### 3. Configuration Pattern
- Environment-based configuration for AWS credentials
- Centralized configuration management through `.env` files
- Runtime configuration for AWS client settings

## Data Flow

### 1. User Input Flow
```
User Input → Streamlit Chat Input → Session State → Claude API → Response Processing → UI Display
```

### 2. Message Processing Flow
1. User enters message in chat input
2. Message added to session state
3. Previous chat history retrieved
4. Full conversation context sent to Claude
5. Response received and parsed
6. Response added to session state
7. UI updated with new message

### 3. Error Handling Flow
```
API Error → Error Classification → Retry Logic → User Notification → Graceful Recovery
```

## Scalability Considerations

### Current Limitations
- Single-threaded Streamlit application
- No horizontal scaling capabilities
- Limited to single user session per instance

### Potential Improvements
- Implement async processing for better performance
- Add connection pooling for AWS clients
- Consider containerization for deployment scaling
- Implement caching for frequently asked questions

## Security Architecture

### Authentication
- AWS IAM-based authentication for Bedrock access
- Environment variable-based credential management
- No user authentication required (public chatbot)

### Data Security
- No persistent storage of user conversations
- Session-based temporary data only
- AWS credentials stored securely in environment variables

### Network Security
- HTTPS communication with AWS services
- No direct database connections
- Stateless application design

## Performance Characteristics

### Response Times
- Typical Claude API response: 2-5 seconds
- UI rendering: Near-instantaneous
- Retry delays: 2, 4, 8, 16, 32 seconds (exponential backoff)

### Resource Usage
- Minimal memory footprint
- CPU usage primarily during API calls
- No persistent storage requirements

## Deployment Architecture

### Development Environment
- Local Streamlit server
- Direct AWS API integration
- Environment file-based configuration

### Production Considerations
- Container deployment (Docker)
- Load balancing for multiple instances
- AWS IAM role-based authentication
- CloudWatch monitoring integration

## Integration Points

### External Dependencies
- **AWS Bedrock**: Core AI model access
- **Streamlit**: Web framework and UI
- **Python-dotenv**: Environment configuration
- **Boto3**: AWS SDK for Python

### API Contracts
- **Claude API**: Anthropic's Bedrock API specification
- **Streamlit API**: Built-in chat components and session state
- **AWS SDK**: Standard AWS service integration patterns
