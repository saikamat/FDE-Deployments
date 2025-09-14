import boto3
import os
from dotenv import load_dotenv

load_dotenv('../.env')

# Initialize Bedrock client
bedrock_client = boto3.client(
    service_name="bedrock",
    region_name=os.getenv("AWS_REGION", "eu-central-1"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
)

try:
    print("Fetching available models...")
    response = bedrock_client.list_foundation_models()
    
    print(f"\nFound {len(response['modelSummaries'])} models:")
    print("-" * 80)
    
    claude_models = []
    for model in response['modelSummaries']:
        model_id = model['modelId']
        provider = model['providerName']
        model_name = model['modelName']
        
        print(f"Model ID: {model_id}")
        print(f"Provider: {provider}")
        print(f"Name: {model_name}")
        print("-" * 80)
        
        # Collect Claude models
        if 'claude' in model_id.lower():
            claude_models.append(model_id)
    
    print(f"\nClaude models found: {claude_models}")
    
except Exception as e:
    print(f"Error: {e}")