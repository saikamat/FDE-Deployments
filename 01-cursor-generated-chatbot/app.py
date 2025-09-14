import os
import json
import streamlit as st
import boto3
import time
from dotenv import load_dotenv
from botocore.exceptions import ClientError

# Load environment variables
load_dotenv()

# Set page config
st.set_page_config(
    page_title="Claude Sonnet QnA Chatbot",
    page_icon="🤖",
    layout="wide"
)

# Configure AWS credentials
aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
aws_region = os.getenv("AWS_REGION", "eu-central-1")

# Initialize Bedrock client with retry configuration
def get_bedrock_client():
    from botocore.config import Config
    
    config = Config(
        retries={
            'max_attempts': 3,
            'mode': 'adaptive'
        }
    )
    
    return boto3.client(
        service_name="bedrock-runtime",
        region_name=aws_region,
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        config=config
    )

# Function to call Claude model via Bedrock with retry logic
def call_claude_model(prompt, chat_history=[]):
    bedrock_client = get_bedrock_client()
    
    # Format messages for Claude
    messages = []
    
    # Add chat history to the messages
    for msg in chat_history:
        role = msg["role"]
        content = msg["content"]
        messages.append({"role": role, "content": content})
    
    # Add the current user message
    messages.append({"role": "user", "content": prompt})
    
    # Prepare request payload for Claude
    request_body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1000,
        "messages": messages,
        "temperature": 0.7,
        "top_p": 0.9,
    }
    
    # Retry logic for throttling
    max_retries = 5
    base_delay = 2  # Start with 2 seconds delay
    
    for attempt in range(max_retries):
        try:
            # Invoke the Claude model
            response = bedrock_client.invoke_model(
                modelId="anthropic.claude-3-sonnet-20240229-v1:0",
                body=json.dumps(request_body)
            )
            
            # Parse the response
            response_body = json.loads(response.get('body').read())
            return response_body.get('content')[0].get('text')
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            
            if error_code == 'ThrottlingException':
                if attempt < max_retries - 1:
                    delay = base_delay * (2 ** attempt)  # Exponential backoff
                    st.warning(f"Rate limited. Retrying in {delay} seconds... (Attempt {attempt + 1}/{max_retries})")
                    time.sleep(delay)
                    continue
                else:
                    raise Exception(f"Rate limit exceeded. Please wait a few minutes before trying again.")
            else:
                raise Exception(f"AWS Error: {str(e)}")
        
        except Exception as e:
            raise Exception(f"Unexpected error: {str(e)}")

# Set up the Streamlit app
def main():
    st.title("🤖 Claude Sonnet QnA Chatbot")
    
    # Add a note about rate limiting
    st.info("💡 **Note**: This chatbot uses AWS Bedrock with rate limiting. If you get throttled, please wait a moment before trying again.")
    
    # Initialize session state for chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat history
    for message in st.session_state.messages:
        role = message["role"]
        content = message["content"]
        with st.chat_message(role):
            st.write(content)
    
    # Input for new question
    if prompt := st.chat_input("Ask me anything..."):
        # Add user message to chat
        user_message = {"role": "user", "content": prompt}
        st.session_state.messages.append(user_message)
        
        # Display the user message
        with st.chat_message("user"):
            st.write(prompt)
        
        # Show a spinner while waiting for the response
        with st.spinner("Thinking..."):
            try:
                # Get Claude's response
                response_text = call_claude_model(prompt, st.session_state.messages[:-1])
                
                # Add AI response to chat
                assistant_message = {"role": "assistant", "content": response_text}
                st.session_state.messages.append(assistant_message)
                
                # Display the assistant message
                with st.chat_message("assistant"):
                    st.write(response_text)
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.session_state.messages.pop()  # Remove the user message if there was an error

if __name__ == "__main__":
    main()