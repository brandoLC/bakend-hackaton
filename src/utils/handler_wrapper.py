import json
import os
import sys

# Añadir directorios al path para importar módulos
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from utils.auth import validate_token
from utils.common import generate_response

def auth_wrapper(handler_function):
    """
    Wrapper para funciones Lambda que valida el token JWT antes de ejecutar la función principal
    
    Args:
        handler_function: La función Lambda a ejecutar si la autenticación es exitosa
        
    Returns:
        function: Función wrapper que verifica la autenticación y luego ejecuta la función original
    """
    def wrapper(event, context):
        # Validar el token JWT
        auth_result = validate_token(event, context)
        
        # Si hay un error en la autenticación, retornar el error
        if auth_result is not None:
            return auth_result
        
        # Si la autenticación es exitosa, ejecutar la función original
        return handler_function(event, context)
    
    return wrapper
