import json
import os
import sys
import boto3
from boto3.dynamodb.conditions import Key

# Importar las utilidades comunes
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.common import generate_response, get_user_id_from_request
from utils.handler_wrapper import auth_wrapper

@auth_wrapper
def handler(event, context):
    """
    Función Lambda para listar todos los diagramas de un usuario
    """
    try:
        # Obtener el ID de usuario
        user_id = get_user_id_from_request(event)
        
        # Inicializar recursos AWS
        dynamodb = boto3.resource('dynamodb')
        diagrams_table = dynamodb.Table(os.environ['DIAGRAMS_TABLE'])
        s3_client = boto3.client('s3')
        bucket_name = os.environ['S3_BUCKET_NAME']
        
        # Consultar los diagramas del usuario usando el índice secundario
        response = diagrams_table.query(
            IndexName='UserIdIndex',
            KeyConditionExpression=Key('userId').eq(user_id)
        )
        
        diagrams = []
        
        # Procesar cada diagrama
        for item in response.get('Items', []):
            # Generar URL presignada para la imagen
            image_url = s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': bucket_name, 'Key': item['imageKey']},
                ExpiresIn=3600  # URL válida por 1 hora
            )
            
            # Generar URL presignada para el código
            code_url = s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': bucket_name, 'Key': item['codeKey']},
                ExpiresIn=3600  # URL válida por 1 hora
            )
            
            diagrams.append({
                'id': item['id'],
                'type': item['type'],
                'createdAt': item['createdAt'],
                'imageUrl': image_url,
                'codeUrl': code_url
            })
        
        # Ordenar por fecha de creación (más recientes primero)
        diagrams.sort(key=lambda x: x['createdAt'], reverse=True)
        
        return generate_response(200, {
            'diagrams': diagrams,
            'count': len(diagrams)
        })
        
    except Exception as e:
        return generate_response(500, {'error': f'Error interno del servidor: {str(e)}'})
