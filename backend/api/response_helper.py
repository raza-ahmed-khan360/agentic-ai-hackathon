"""
Vercel serverless response helper.
Converts Python responses to Vercel HTTP format.
"""

import json


def json_response(data, status_code=200, headers=None):
    """
    Create a Vercel-compatible JSON response.
    
    This is what Vercel serverless functions should return.
    """
    default_headers = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, Authorization",
    }
    
    if headers:
        default_headers.update(headers)
    
    # Vercel expects this format
    return {
        "statusCode": status_code,
        "headers": default_headers,
        "body": json.dumps(data) if not isinstance(data, str) else data,
    }


def error_response(message, status_code=500):
    """Create an error response."""
    return json_response({"error": message}, status_code=status_code)


def parse_body(event):
    """Parse request body from Vercel event."""
    try:
        if isinstance(event.get("body"), str):
            return json.loads(event["body"])
        return event.get("body", {})
    except:
        return {}
