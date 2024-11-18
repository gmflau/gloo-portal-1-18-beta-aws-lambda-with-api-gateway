# Sample Lambda function to return static responses
 
import json
from typing import Dict, Any

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    try:
        path = event.get('path', '')
        http_method = event.get('httpMethod', '')
        
        if path == '/hello' and http_method == 'GET':
            return build_response(200, 'Hello, World!')
        elif path == '/health' and http_method == 'GET':
            return build_response(200, 'OK')
        else:
            return build_response(404, 'Not Found')
            
    except Exception as e:
        print(f"Error: {str(e)}")
        return build_response(500, 'Internal Server Error')

def build_response(status_code: int, body: Dict[str, str]) -> Dict[str, Any]:
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Content-Type'
        },
        'body': json.dumps(body)
    }