#!/usr/bin/env python3
"""
Script para generar diagramas ER a partir de código Python.
Este script es llamado por las funciones Lambda para generar diagramas.
"""

import sys
import os
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey
from eralchemy2 import render_er

def generate_diagram(code_file, output_file):
    """
    Genera un diagrama ER a partir de un archivo Python.
    
    Args:
        code_file (str): Ruta al archivo con el código Python del diagrama
        output_file (str): Ruta donde se guardará la imagen generada
    """
    try:
        # Crear un motor de base de datos en memoria
        engine = create_engine('sqlite:///:memory:')
        metadata = MetaData()
        
        # Ejecutar el código del archivo para definir las tablas
        with open(code_file, 'r') as f:
            code = f.read()
            exec(code)
        
        # Generar el diagrama ER
        render_er(metadata, output_file)
        
        return True
    except Exception as e:
        print(f"Error generando diagrama ER: {str(e)}")
        return False

if __name__ == "__main__":
    # Verificar argumentos
    if len(sys.argv) < 3:
        print("Uso: generate_er_diagram.py <archivo_codigo> <archivo_salida>")
        sys.exit(1)
    
    # Obtener argumentos
    code_file = sys.argv[1]
    output_file = sys.argv[2]
    
    # Generar diagrama
    success = generate_diagram(code_file, output_file)
    
    # Salir con código de error si hubo problemas
    sys.exit(0 if success else 1)
