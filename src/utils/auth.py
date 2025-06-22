import json
import os
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

def validate_token(event, context):
    """
    Middleware para validar tokens JWT en las solicitudes
    """
    try:
        # Obtener el token del header Authorization
        auth_header = event.get('headers', {}).get('Authorization')
        
        if not auth_header:
            return {
                'statusCode': 401,
                'body': json.dumps({'error': 'Token no proporcionado'})
            }
        
        # Extraer el token (formato "Bearer <token>")
        if auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
        else:
            token = auth_header
        
        # Verificar y decodificar el token
        # Nota: En producción, obtén la clave secreta de un lugar seguro (ej. AWS Secrets Manager)
        secret_key = os.environ.get('JWT_SECRET', 'your-default-secret-key')
        decoded = jwt.decode(token, secret_key, algorithms=['HS256'])
        
        # Agregar la información del usuario al evento para que sea accesible en las funciones Lambda
        event['user'] = {
            'userId': decoded.get('user_id'),
            'email': decoded.get('email'),
            'name': decoded.get('name')
        }
        
        # Continuar con la ejecución de la función
        return None
        
    except ExpiredSignatureError:
        return {
            'statusCode': 401,
            'body': json.dumps({'error': 'Token expirado'})
        }
    except InvalidTokenError:
        return {
            'statusCode': 401,
            'body': json.dumps({'error': 'Token inválido'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f'Error al validar token: {str(e)}'})
        }
