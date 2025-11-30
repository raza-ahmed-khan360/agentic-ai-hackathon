# Test simple Vercel serverless format
import json

# This is the ONLY correct format Vercel accepts
def handler(event, context):
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        },
        "body": json.dumps({"status": "Agentic AI Backend is Running"})
    }
