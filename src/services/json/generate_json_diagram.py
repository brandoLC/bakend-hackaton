#!/usr/bin/env python3
"""
Script para generar diagramas de estructuras JSON.
Este script es llamado por las funciones Lambda para generar diagramas.
"""

import sys
import os
import json
import networkx as nx
import matplotlib.pyplot as plt

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

def generate_diagram(json_file, output_file):
    """
    Genera un diagrama de estructura JSON a partir de un archivo.
    
    Args:
        json_file (str): Ruta al archivo con el JSON
        output_file (str): Ruta donde se guardará la imagen generada
    """
    try:
        # Leer el JSON del archivo
        with open(json_file, 'r') as f:
            json_str = f.read()
            json_data = json.loads(json_str)
        
        # Generar un grafo a partir del JSON
        graph = generate_json_graph(json_data)
        
        # Crear la figura
        plt.figure(figsize=(12, 8))
        pos = nx.spring_layout(graph)
        nx.draw(graph, pos, with_labels=True, node_color='skyblue', 
                node_size=1500, edge_color='gray', linewidths=1, 
                font_size=10, arrows=True)
        
        plt.title('Estructura JSON')
        plt.axis('off')
        
        # Guardar la figura
        plt.savefig(output_file, format='png', dpi=300, bbox_inches='tight')
        plt.close()
        
        return True
    except Exception as e:
        print(f"Error generando diagrama JSON: {str(e)}")
        return False

if __name__ == "__main__":
    # Verificar argumentos
    if len(sys.argv) < 3:
        print("Uso: generate_json_diagram.py <archivo_json> <archivo_salida>")
        sys.exit(1)
    
    # Obtener argumentos
    json_file = sys.argv[1]
    output_file = sys.argv[2]
    
    # Generar diagrama
    success = generate_diagram(json_file, output_file)
    
    # Salir con código de error si hubo problemas
    sys.exit(0 if success else 1)
