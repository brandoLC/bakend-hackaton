#!/usr/bin/env python3
"""
Script para generar diagramas de AWS a partir de código Python.
Este script es llamado por las funciones Lambda para generar diagramas.
"""

import sys
import os
from diagrams import Diagram
from diagrams.aws.compute import EC2, Lambda
from diagrams.aws.database import RDS, DynamoDB
from diagrams.aws.network import VPC, APIGateway
from diagrams.aws.storage import S3
from diagrams.aws.security import IAM, Cognito
from diagrams.aws.integration import SQS
from diagrams.aws.management import CloudWatch

def generate_diagram(code_file, output_file):
    """
    Genera un diagrama AWS a partir de un archivo Python.
    
    Args:
        code_file (str): Ruta al archivo con el código Python del diagrama
        output_file (str): Ruta donde se guardará la imagen generada
    """
    try:
        # Configurar variables de entorno para diagrams
        os.environ["PATH"] += os.pathsep + '/usr/local/bin/'
        
        # Obtener formato de salida
        output_format = output_file.split('.')[-1]
        output_name = output_file.split('/')[-1].split('.')[0]
        
        # Configurar diagrams para usar el formato y nombre especificados
        os.environ["DIAGRAM_FILENAME"] = output_name
        os.environ["DIAGRAM_FORMAT"] = output_format
        
        # Guardar el directorio actual
        original_dir = os.getcwd()
        
        # Cambiar al directorio del archivo de salida
        output_dir = os.path.dirname(output_file)
        if output_dir:
            os.chdir(output_dir)
        
        # Ejecutar el código del archivo
        with open(code_file, 'r') as f:
            code = f.read()
            exec(code)
        
        # Volver al directorio original
        os.chdir(original_dir)
        
        return True
    except Exception as e:
        print(f"Error generando diagrama: {str(e)}")
        return False

if __name__ == "__main__":
    # Verificar argumentos
    if len(sys.argv) < 3:
        print("Uso: generate_aws_diagram.py <archivo_codigo> <archivo_salida>")
        sys.exit(1)
    
    # Obtener argumentos
    code_file = sys.argv[1]
    output_file = sys.argv[2]
    
    # Generar diagrama
    success = generate_diagram(code_file, output_file)
    
    # Salir con código de error si hubo problemas
    sys.exit(0 if success else 1)
