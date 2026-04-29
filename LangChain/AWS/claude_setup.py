import boto3
import json
prompt_data=""" 
Act as a mathematican and explain Generative AI
"""

bedrock=boto3.client(service_name="bedrock-runtime",region_name='us-east-1')

payload={
    "prompt":prompt_data,
    "maxTokens":120,
    "temperature":0.8,
    "topP":0.8
}
body=json.dumps(payload)
model_id="amazon.nova-micro-v1:0"
response=bedrock.invoke_model(
    body=body,
    modelId=model_id,
    accept="application/json",
    contentType="application/json"
)
response_body=json.loads(response.get("body").read())
response_text=response_body.get("completions")[0].get("data").get("text")
print("response:",response_text)