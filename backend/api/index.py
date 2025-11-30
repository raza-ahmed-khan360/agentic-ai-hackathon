import json

def handler(request):
	"""Vercel serverless handler for root endpoint - health check"""
	return {
		"statusCode": 200,
		"headers": {
			"Content-Type": "application/json",
			"Access-Control-Allow-Origin": "*",
		},
		"body": json.dumps({
			"status": "Agentic AI Backend is Running"
		})
	}