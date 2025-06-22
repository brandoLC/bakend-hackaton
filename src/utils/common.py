import json
import boto3
import uuid
import os
import base64
from datetime import datetime

# Inicialización de recursos AWS
s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
diagrams_table = dynamodb.Table(os.environ['DIAGRAMS_TABLE'])
bucket_name = os.environ['S3_BUCKET_NAME']

def generate_response(status_code, body):
    """
    Genera una respuesta formateada para API Gateway
    """
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': True,
        },
        'body': json.dumps(body)
    }

def save_diagram(diagram_data, user_id, diagram_type, code):
    """
    Guarda un diagrama en S3 y sus metadatos en DynamoDB
    
    Args:
        diagram_data (bytes): Imagen del diagrama en formato bytes
        user_id (str): ID del usuario
        diagram_type (str): Tipo de diagrama (aws, er, json)
        code (str): Código fuente del diagrama
        
    Returns:
        dict: Información del diagrama guardado
    """
    # Generar ID único para el diagrama
    diagram_id = str(uuid.uuid4())
    timestamp = datetime.now().isoformat()
    
    # Nombre de archivos en S3
    image_key = f"{user_id}/{diagram_type}/{diagram_id}.png"
    code_key = f"{user_id}/{diagram_type}/{diagram_id}.txt"
    
    # Guardar imagen en S3
    s3_client.put_object(
        Bucket=bucket_name,
        Key=image_key,
        Body=diagram_data,
        ContentType='image/png'
    )
    
    # Guardar código fuente en S3
    s3_client.put_object(
        Bucket=bucket_name,
        Key=code_key,
        Body=code,
        ContentType='text/plain'
    )
    
    # Generar URLs presignadas para acceso temporal
    image_url = s3_client.generate_presigned_url(
        'get_object',
        Params={'Bucket': bucket_name, 'Key': image_key},
        ExpiresIn=3600  # URL válida por 1 hora
    )
    
    # Guardar metadatos en DynamoDB
    item = {
        'id': diagram_id,
        'userId': user_id,
        'type': diagram_type,
        'createdAt': timestamp,
        'imageKey': image_key,
        'codeKey': code_key
    }
    
    diagrams_table.put_item(Item=item)
    
    return {
        'id': diagram_id,
        'type': diagram_type,
        'createdAt': timestamp,
        'imageUrl': image_url
    }

def get_user_id_from_request(event):
    """
    Extrae el ID de usuario de la petición
    En este caso, lo obtenemos del objeto user que se agrega durante la validación del token
    """
    # Obtener la información del usuario del objeto event (agregado por el middleware de autenticación)
    user = event.get('user', {})
    return user.get('userId', 'anonymous')
