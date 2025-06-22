# Servicio para manejar diagramas JSON
# Aquí puedes añadir funciones más específicas para procesar diagramas JSON

def parse_json_code(json_str):
    """
    Analiza el código JSON y valida su estructura
    """
    # Implementación futura: validación del JSON
    try:
        import json
        json.loads(json_str)
        return True
    except:
        return False

def get_json_diagram_example():
    """
    Devuelve un ejemplo de código JSON para un diagrama
    """
    return """
{
  "application": "UTEC Diagram",
  "version": "1.0.0",
  "components": {
    "frontend": {
      "type": "web",
      "technologies": ["React", "TypeScript", "AWS Amplify"],
      "features": ["Editor de código", "Visualización de diagramas", "Exportación"]
    },
    "backend": {
      "type": "serverless",
      "services": [
        {
          "name": "API Gateway",
          "purpose": "Exposición de APIs"
        },
        {
          "name": "Lambda",
          "purpose": "Procesamiento de diagramas",
          "functions": ["AWS Diagrams", "ER Diagrams", "JSON Diagrams"]
        },
        {
          "name": "S3",
          "purpose": "Almacenamiento de diagramas"
        },
        {
          "name": "DynamoDB",
          "purpose": "Metadatos de diagramas"
        }
      ]
    },
    "authentication": {
      "service": "Cognito",
      "features": ["Login", "Registro", "Autorización"]
    }
  },
  "data": {
    "storage": {
      "diagrams": "S3 Bucket",
      "metadata": "DynamoDB Table"
    },
    "formats": ["PNG", "SVG", "PDF"]
  }
}
"""
