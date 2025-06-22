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
    Función Lambda para generar diagramas Entidad-Relación
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
        
        # Crear un archivo temporal para el script SQL o la definición del modelo
        with tempfile.NamedTemporaryFile(suffix='.py', delete=False) as tmp_file:
            # Preparar el código para generar el diagrama ER
            er_code = f"""
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey
from eralchemy2 import render_er
import os

# Crear un motor de base de datos en memoria
engine = create_engine('sqlite:///:memory:')
metadata = MetaData()

# Ejecutar el código del usuario para definir las tablas
{code}

# Generar el diagrama ER
output_path = 'er_diagram.png'
render_er(metadata, output_path)
"""
            # Escribir el código al archivo temporal
            tmp_file.write(er_code.encode('utf-8'))
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
                with open('er_diagram.png', 'rb') as f:
                    diagram_data = f.read()
            except Exception as e:
                return generate_response(400, {'error': f'Error al generar el diagrama: {str(e)}'})
            finally:
                # Restaurar el directorio de trabajo
                os.chdir(original_dir)
                # Eliminar el archivo temporal
                os.unlink(tmp_file_path)
        
        # Guardar el diagrama en S3 y los metadatos en DynamoDB
        diagram_info = save_diagram(diagram_data, user_id, 'er', code)
        
        # Devolver la información del diagrama, incluyendo la URL para acceder a él
        return generate_response(200, {
            'message': 'Diagrama generado con éxito',
            'diagram': diagram_info,
            'imageBase64': base64.b64encode(diagram_data).decode('utf-8')
        })
        
    except Exception as e:
        return generate_response(500, {'error': f'Error interno del servidor: {str(e)}'})
