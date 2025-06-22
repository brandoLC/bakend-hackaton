import json
import os
import sys
import tempfile
import base64
import networkx as nx
import matplotlib.pyplot as plt
from io import BytesIO

# Importar las utilidades comunes
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.common import generate_response, save_diagram, get_user_id_from_request

def generate_json_graph(json_data, graph=None, parent=None, parent_name=None):
    """
    Genera un grafo a partir de datos JSON
    """
    if graph is None:
        graph = nx.DiGraph()
    
    # Si es un diccionario, procesar cada clave-valor
    if isinstance(json_data, dict):
        for key, value in json_data.items():
            node_name = f"{parent_name}.{key}" if parent_name else key
            
            if parent:
                graph.add_edge(parent, node_name)
            else:
                graph.add_node(node_name)
                
            generate_json_graph(value, graph, node_name, node_name)
    
    # Si es una lista, procesar cada elemento
    elif isinstance(json_data, list):
        for i, item in enumerate(json_data):
            node_name = f"{parent_name}[{i}]" if parent_name else f"[{i}]"
            
            if parent:
                graph.add_edge(parent, node_name)
            else:
                graph.add_node(node_name)
                
            generate_json_graph(item, graph, node_name, node_name)
    
    # Si es un valor primitivo, simplemente añadir el nodo
    else:
        node_name = f"{parent_name}={json_data}" if parent_name else str(json_data)
        
        if parent:
            graph.add_edge(parent, node_name)
        else:
            graph.add_node(node_name)
    
    return graph

from utils.handler_wrapper import auth_wrapper

@auth_wrapper
def generate(event, context):
    """
    Función Lambda para generar diagramas de estructura JSON
    """
    try:
        # Validar que haya un cuerpo en la petición
        if not event.get('body'):
            return generate_response(400, {'error': 'Se requiere el cuerpo de la petición'})
        
        # Parsear el cuerpo de la petición
        body = json.loads(event['body'])
        
        # Validar que exista el código JSON
        if 'code' not in body:
            return generate_response(400, {'error': 'Se requiere el código JSON del diagrama'})
        
        json_code = body['code']
        
        # Obtener el ID de usuario
        user_id = get_user_id_from_request(event)
        
        try:
            # Parsear el JSON proporcionado
            json_data = json.loads(json_code)
        except json.JSONDecodeError as e:
            return generate_response(400, {'error': f'JSON inválido: {str(e)}'})
        
        # Generar un grafo a partir del JSON
        graph = generate_json_graph(json_data)
        
        # Crear un archivo para guardar la imagen
        with BytesIO() as img_data:
            plt.figure(figsize=(12, 8))
            pos = nx.spring_layout(graph)
            nx.draw(graph, pos, with_labels=True, node_color='skyblue', 
                    node_size=1500, edge_color='gray', linewidths=1, 
                    font_size=10, arrows=True)
            
            plt.title('Estructura JSON')
            plt.axis('off')
            
            # Guardar la figura en el objeto BytesIO
            plt.savefig(img_data, format='png', dpi=300, bbox_inches='tight')
            plt.close()
            
            # Obtener los bytes de la imagen
            img_data.seek(0)
            diagram_data = img_data.read()
        
        # Guardar el diagrama en S3 y los metadatos en DynamoDB
        diagram_info = save_diagram(diagram_data, user_id, 'json', json_code)
        
        # Devolver la información del diagrama, incluyendo la URL para acceder a él
        return generate_response(200, {
            'message': 'Diagrama generado con éxito',
            'diagram': diagram_info,
            'imageBase64': base64.b64encode(diagram_data).decode('utf-8')
        })
        
    except Exception as e:
        return generate_response(500, {'error': f'Error interno del servidor: {str(e)}'})
