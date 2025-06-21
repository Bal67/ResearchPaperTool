import boto3
import json
import os

bedrock = boto3.client("bedrock-runtime", region_name=os.getenv("AWS_REGION", "us-east-1"))

def call_claude(prompt: str, max_tokens: int = 1024, temperature: float = 0.7) -> str:
    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "max_tokens": max_tokens,
        "temperature": temperature,
        "top_k": 250,
        "top_p": 1.0,
        "stop_sequences": []
    }

    response = bedrock.invoke_model(
        modelId="anthropic.claude-3-sonnet-20240229-v1:0",
        body=json.dumps(body),
        contentType="application/json",
        accept="application/json"
    )
    
    result = json.loads(response["body"].read())
    return result["content"][0]["text"]
