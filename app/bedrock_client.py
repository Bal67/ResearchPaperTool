import boto3
import json

def call_claude(prompt: str) -> str:
    client = boto3.client("bedrock-runtime", region_name="us-east-1")

    body = {
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 1024,
        "temperature": 0.5,
        "anthropic_version": "bedrock-2023-05-31"
    }

    response = client.invoke_model(
        modelId="anthropic.claude-3-sonnet-20240229-v1:0",
        contentType="application/json",
        accept="application/json",
        body=json.dumps(body),
    )

    result = json.loads(response["body"].read())
    return result["content"][0]["text"]
