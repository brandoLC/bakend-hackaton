# UTEC Diagram API

API serverless para la generación, edición y visualización de diagramas técnicos a partir de definiciones escritas como código.

## Descripción

UTEC Diagram es una herramienta basada en el concepto "Diagram as Code", que permite la creación de diagramas técnicos a partir de código. Esta API soporta la generación de tres tipos principales de diagramas:

1. **Diagramas de AWS**: Representaciones visuales de arquitecturas en la nube AWS.
2. **Diagramas Entidad-Relación (ER)**: Visualización de estructuras de bases de datos.
3. **Diagramas JSON**: Representación gráfica de estructuras de datos JSON.

## Tecnologías

- **AWS Lambda**: Funciones serverless para el procesamiento de diagramas
- **API Gateway**: Exposición de APIs REST
- **S3**: Almacenamiento de diagramas generados
- **DynamoDB**: Metadatos de diagramas
- **Python 3.13**: Lenguaje de programación

## Estructura del Proyecto

```
api-diagrmas/
├── requirements.txt (dependencias de Python)
├── serverless.yml (configuración de Serverless Framework)
└── src/
    ├── functions/
    │   ├── aws_diagrams.py (generación de diagramas AWS)
    │   ├── er_diagrams.py (generación de diagramas ER)
    │   ├── json_diagrams.py (generación de diagramas JSON)
    │   └── list_diagrams.py (listado de diagramas)
    ├── services/
    │   ├── aws/ (servicios específicos para AWS)
    │   ├── er/ (servicios específicos para ER)
    │   └── json/ (servicios específicos para JSON)
    └── utils/
        ├── auth.py (autenticación JWT)
        ├── common.py (utilidades comunes)
        └── handler_wrapper.py (middleware de autenticación)
```

## Endpoints de la API

- **POST /diagrams/aws**: Genera un diagrama de arquitectura AWS
- **POST /diagrams/er**: Genera un diagrama Entidad-Relación
- **POST /diagrams/json**: Genera un diagrama de estructura JSON
- **GET /diagrams**: Lista todos los diagramas del usuario autenticado

## Autenticación

La API utiliza autenticación basada en tokens JWT. Cada solicitud debe incluir un token válido en el encabezado `Authorization`.

## Instalación y Despliegue

### Requisitos previos

- Node.js y npm instalados
- Serverless Framework instalado: `npm install -g serverless`
- Python 3.13 instalado
- Cuenta AWS configurada

### Instalación de dependencias

```bash
pip install -r requirements.txt
```

### Despliegue

```bash
serverless deploy
```

## Ejemplos de Uso

### Ejemplo de diagrama AWS

```python
with Diagram("Arquitectura Serverless", show=False):
    cognito = Cognito("Autenticación")
    api = APIGateway("API Gateway")
    auth_lambda = Lambda("Autorización")
    process_lambda = Lambda("Procesamiento")
    dynamo = DynamoDB("Metadatos")
    bucket = S3("Almacenamiento de Diagramas")
    monitor = CloudWatch("Monitoreo")

    cognito >> auth_lambda >> api
    api >> process_lambda
    process_lambda >> dynamo
    process_lambda >> bucket
    process_lambda >> monitor
```

### Ejemplo de diagrama ER

```python
users = Table('users', metadata,
    Column('id', Integer, primary_key=True),
    Column('username', String(50), nullable=False),
    Column('email', String(100), nullable=False)
)

posts = Table('posts', metadata,
    Column('id', Integer, primary_key=True),
    Column('title', String(100), nullable=False),
    Column('user_id', Integer, ForeignKey('users.id'))
)
```

### Ejemplo de diagrama JSON

```json
{
  "application": "UTEC Diagram",
  "components": {
    "frontend": {
      "type": "web",
      "technologies": ["React", "TypeScript"]
    },
    "backend": {
      "type": "serverless",
      "services": ["Lambda", "API Gateway", "S3", "DynamoDB"]
    }
  }
}
```

## Licencia

MIT
