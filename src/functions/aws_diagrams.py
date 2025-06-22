import json
import os
import sys
import tempfile
import base64
from io import BytesIO

# Importar las utilidades comunes
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.common import generate_response, save_diagram, get_user_id_from_request
from utils.handler_wrapper import auth_wrapper

@auth_wrapper
def generate(event, context):
    """
    Función Lambda para generar diagramas de arquitectura AWS
    """
    try:
        # Validar que haya un cuerpo en la petición
        if not event.get('body'):
            return generate_response(400, {'error': 'Se requiere el cuerpo de la petición'})
        
        # Parsear el cuerpo de la petición
        body = json.loads(event['body'])
        
        # Validar que exista el código
        if 'code' not in body:
            return generate_response(400, {'error': 'Se requiere el código del diagrama'})
        
        code = body['code']
        
        # Obtener el ID de usuario
        user_id = get_user_id_from_request(event)
        
        # Generar un archivo temporal para ejecutar el código del diagrama
        with tempfile.NamedTemporaryFile(suffix='.py', delete=False) as tmp_file:
            # Preparar el código Python para generar el diagrama
            diagram_code = f"""
import os
from diagrams import Diagram
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import VPC
from diagrams.aws.storage import S3
from diagrams.aws.security import IAM
from diagrams.aws.integration import SQS
from diagrams.aws.management import CloudWatch
from diagrams.aws.compute import Lambda
from diagrams.aws.network import APIGateway
from diagrams.aws.mobile import Cognito
from diagrams.aws.database import DynamoDB

# Configurar diagrams para generar imagen sin abrir una ventana
os.environ["PATH"] += os.pathsep + '/usr/local/bin/'
os.environ["DIAGRAM_FILENAME"] = "aws_diagram"
os.environ["DIAGRAM_FORMAT"] = "png"

# Ejecutar el código del usuario
{code}
"""
            # Escribir el código al archivo temporal
            tmp_file.write(diagram_code.encode('utf-8'))
            tmp_file.flush()
            tmp_file_path = tmp_file.name
        
        # Directorio temporal para guardar la imagen generada
        with tempfile.TemporaryDirectory() as output_dir:
            # Establecer el directorio de trabajo
            original_dir = os.getcwd()
            os.chdir(output_dir)
            
            try:
                # Ejecutar el código para generar el diagrama
                exec(open(tmp_file_path).read())
                
                # Leer el archivo de imagen generado
                with open('aws_diagram.png', 'rb') as f:
                    diagram_data = f.read()
            except Exception as e:
                return generate_response(400, {'error': f'Error al generar el diagrama: {str(e)}'})
            finally:
                # Restaurar el directorio de trabajo
                os.chdir(original_dir)
                # Eliminar el archivo temporal
                os.unlink(tmp_file_path)
        
        # Guardar el diagrama en S3 y los metadatos en DynamoDB
        diagram_info = save_diagram(diagram_data, user_id, 'aws', code)
        
        # Devolver la información del diagrama, incluyendo la URL para acceder a él
        return generate_response(200, {
            'message': 'Diagrama generado con éxito',
            'diagram': diagram_info,
            'imageBase64': base64.b64encode(diagram_data).decode('utf-8')
        })
        
    except Exception as e:
        return generate_response(500, {'error': f'Error interno del servidor: {str(e)}'})
