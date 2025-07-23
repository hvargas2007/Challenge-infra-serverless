import json
import os
import uuid
from datetime import datetime
from pathlib import Path
import fcntl

EFS_PATH = os.environ.get('EFS_PATH', '/mnt/efs')
JSON_STORAGE_PATH = Path(EFS_PATH) / "json-storage"

# Ensure storage directory exists
JSON_STORAGE_PATH.mkdir(parents=True, exist_ok=True)

def get_server_id():
    return os.environ.get('AWS_LAMBDA_FUNCTION_NAME', 'lambda-instance')

def handler(event, context):
    """Lambda handler for API Gateway proxy integration"""
    try:
        path = event.get('path', '')
        method = event.get('httpMethod', '')
        headers = {k.lower(): v for k, v in event.get('headers', {}).items()}
        path_parameters = event.get('pathParameters', {})
        
        # Route handling
        if path == '/':
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({
                    'message': 'Welcome to the JSON Storage API',
                    'endpoints': {
                        'GET /': 'This message',
                        'GET /health': 'Health check',
                        'POST /json': 'Create new JSON document',
                        'GET /json/{id}': 'Get JSON document',
                        'PUT /json/{id}': 'Update JSON document',
                        'DELETE /json/{id}': 'Delete JSON document'
                    }
                })
            }
        
        elif path == '/health':
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({
                    'status': 'healthy',
                    'server_id': get_server_id(),
                    'timestamp': datetime.utcnow().isoformat()
                })
            }
        
        elif path == '/json' and method == 'POST':
            try:
                body = json.loads(event.get('body', '{}'))
                if not isinstance(body, dict) or 'data' not in body:
                    return {
                        'statusCode': 400,
                        'body': json.dumps({'error': 'Request body must contain "data" field'})
                    }
                
                doc_id = str(uuid.uuid4())
                file_path = JSON_STORAGE_PATH / f"{doc_id}.json"
                
                document = {
                    'id': doc_id,
                    'data': body['data'],
                    'created_at': datetime.utcnow().isoformat(),
                    'created_by': get_server_id()
                }
                
                with open(file_path, 'w') as f:
                    fcntl.flock(f, fcntl.LOCK_EX)
                    json.dump(document, f)
                    fcntl.flock(f, fcntl.LOCK_UN)
                
                return {
                    'statusCode': 201,
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps(document)
                }
            except json.JSONDecodeError:
                return {
                    'statusCode': 400,
                    'body': json.dumps({'error': 'Invalid JSON in request body'})
                }
        
        elif path.startswith('/json/') and method == 'GET':
            doc_id = path_parameters.get('id', '')
            if not doc_id:
                return {
                    'statusCode': 400,
                    'body': json.dumps({'error': 'Document ID required'})
                }
            
            file_path = JSON_STORAGE_PATH / f"{doc_id}.json"
            
            if not file_path.exists():
                return {
                    'statusCode': 404,
                    'body': json.dumps({'error': 'Document not found'})
                }
            
            with open(file_path, 'r') as f:
                fcntl.flock(f, fcntl.LOCK_SH)
                document = json.load(f)
                fcntl.flock(f, fcntl.LOCK_UN)
            
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps(document)
            }
        
        elif path.startswith('/json/') and method == 'PUT':
            doc_id = path_parameters.get('id', '')
            if not doc_id:
                return {
                    'statusCode': 400,
                    'body': json.dumps({'error': 'Document ID required'})
                }
            
            file_path = JSON_STORAGE_PATH / f"{doc_id}.json"
            
            if not file_path.exists():
                return {
                    'statusCode': 404,
                    'body': json.dumps({'error': 'Document not found'})
                }
            
            try:
                body = json.loads(event.get('body', '{}'))
                if not isinstance(body, dict) or 'data' not in body:
                    return {
                        'statusCode': 400,
                        'body': json.dumps({'error': 'Request body must contain "data" field'})
                    }
                
                with open(file_path, 'r+') as f:
                    fcntl.flock(f, fcntl.LOCK_EX)
                    document = json.load(f)
                    document['data'] = body['data']
                    document['updated_at'] = datetime.utcnow().isoformat()
                    document['updated_by'] = get_server_id()
                    f.seek(0)
                    json.dump(document, f)
                    f.truncate()
                    fcntl.flock(f, fcntl.LOCK_UN)
                
                return {
                    'statusCode': 200,
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps(document)
                }
            except json.JSONDecodeError:
                return {
                    'statusCode': 400,
                    'body': json.dumps({'error': 'Invalid JSON in request body'})
                }
        
        elif path.startswith('/json/') and method == 'DELETE':
            doc_id = path_parameters.get('id', '')
            if not doc_id:
                return {
                    'statusCode': 400,
                    'body': json.dumps({'error': 'Document ID required'})
                }
            
            file_path = JSON_STORAGE_PATH / f"{doc_id}.json"
            
            if not file_path.exists():
                return {
                    'statusCode': 404,
                    'body': json.dumps({'error': 'Document not found'})
                }
            
            file_path.unlink()
            
            return {
                'statusCode': 204,
                'body': ''
            }
        
        else:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'Not found'})
            }
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal server error'})
        }