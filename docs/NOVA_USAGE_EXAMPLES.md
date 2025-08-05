# Amazon Nova Models - Usage Examples

Esta documentación proporciona ejemplos prácticos y detallados de cómo usar los modelos Amazon Nova con el servidor MCP Crawl4AI RAG.

## Tabla de Contenidos

1. [Configuración Básica](#configuración-básica)
2. [Ejemplos por Modelo](#ejemplos-por-modelo)
3. [Casos de Uso Prácticos](#casos-de-uso-prácticos)
4. [Comparación de Costos](#comparación-de-costos)
5. [Migración desde Claude](#migración-desde-claude)
6. [Troubleshooting](#troubleshooting)

## Configuración Básica

### Estructura del Request Body para Nova

Los modelos Nova utilizan el siguiente formato de request:

```json
{
  "messages": [
    {"role": "user", "content": "Tu prompt aquí"}
  ],
  "max_tokens": 2048,
  "temperature": 0.7,
  "top_p": 0.9
}
```

### Estructura del Response Body de Nova

Los modelos Nova devuelven respuestas en este formato:

```json
{
  "output": {
    "message": {
      "content": [
        {"text": "Respuesta generada del modelo"}
      ]
    }
  }
}
```

## Ejemplos por Modelo

### 1. Amazon Nova Micro (`amazon.nova-micro-v1:0`)

**Características:**
- Modelo de texto únicamente
- Optimizado para el menor costo y latencia
- Ideal para tareas simples de generación de contexto

**Configuración:**

```bash
# .env
CONTEXT_PROVIDER="bedrock"
BEDROCK_CONTEXT_MODEL_ID="amazon.nova-micro-v1:0"
AWS_REGION="us-east-1"
AWS_ACCESS_KEY_ID="tu_access_key"
AWS_SECRET_ACCESS_KEY="tu_secret_key"
```

**Ejemplo de Uso en Código:**

```python
from providers.aws_bedrock import invoke_bedrock_model

# Configuración para Nova Micro
model_id = "amazon.nova-micro-v1:0"
prompt = "Proporciona un resumen conciso de este documento para mejorar la búsqueda vectorial."

result = invoke_bedrock_model(
    model_id=model_id,
    prompt=prompt,
    max_tokens=150,  # Mantener bajo para costos
    temperature=0.3,  # Baja para consistencia
    top_p=0.8
)

print(f"Contexto generado: {result}")
```

**Casos de Uso Ideales:**
- Generación de contexto para embeddings
- Resúmenes simples de documentos
- Clasificación básica de texto
- Extracción de palabras clave

### 2. Amazon Nova Lite (`amazon.nova-lite-v1:0`)

**Características:**
- Modelo multimodal (texto, imágenes, video)
- Rápido y económico
- Buena relación calidad-precio

**Configuración:**

```bash
# .env
CONTEXT_PROVIDER="bedrock"
BEDROCK_CONTEXT_MODEL_ID="amazon.nova-lite-v1:0"
```

**Ejemplo de Uso:**

```python
# Para análisis de contenido multimodal
model_id = "amazon.nova-lite-v1:0"
prompt = "Analiza este documento y extrae los conceptos clave para mejorar la búsqueda semántica."

result = invoke_bedrock_model(
    model_id=model_id,
    prompt=prompt,
    max_tokens=300,
    temperature=0.5,
    top_p=0.9
)
```

**Casos de Uso Ideales:**
- Análisis de documentos con imágenes
- Procesamiento rápido de contenido mixto
- Generación de metadatos enriquecidos

### 3. Amazon Nova Pro (`amazon.nova-pro-v1:0`)

**Características:**
- Modelo multimodal avanzado
- Alta calidad en tareas complejas
- Mejor para análisis sofisticados

**Configuración:**

```bash
# .env
CONTEXT_PROVIDER="bedrock"
BEDROCK_CONTEXT_MODEL_ID="amazon.nova-pro-v1:0"
```

**Ejemplo de Uso:**

```python
# Para análisis complejo de documentos
model_id = "amazon.nova-pro-v1:0"
prompt = """
Analiza este documento técnico y genera un contexto detallado que incluya:
1. Conceptos técnicos principales
2. Relaciones entre ideas
3. Términos especializados
4. Contexto de aplicación
"""

result = invoke_bedrock_model(
    model_id=model_id,
    prompt=prompt,
    max_tokens=500,
    temperature=0.4,
    top_p=0.85
)
```

## Casos de Uso Prácticos

### Caso 1: Startup con Presupuesto Limitado

**Escenario:** Una startup necesita procesamiento RAG económico para su base de conocimientos.

**Solución con Nova Micro:**

```bash
# docker-compose.yml
version: '3.8'
services:
  crawl4ai-rag:
    image: ignaciocardenas/mcp-crawl4ai-rag-softworks:latest
    environment:
      - CONTEXT_PROVIDER=bedrock
      - BEDROCK_CONTEXT_MODEL_ID=amazon.nova-micro-v1:0
      - EMBEDDINGS_PROVIDER=openai  # O usar Bedrock Titan
      - AWS_REGION=us-east-1
    ports:
      - "8051:8051"
```

**Beneficios:**
- Costo reducido hasta 80% vs Claude
- Latencia mejorada
- Calidad suficiente para contexto básico

### Caso 2: Empresa con Contenido Multimodal

**Escenario:** Empresa que procesa documentos técnicos con diagramas e imágenes.

**Solución con Nova Lite:**

```python
# Configuración específica para documentos multimodales
import os

os.environ['CONTEXT_PROVIDER'] = 'bedrock'
os.environ['BEDROCK_CONTEXT_MODEL_ID'] = 'amazon.nova-lite-v1:0'

# El sistema automáticamente usará Nova Lite para generar contexto
# de documentos que contengan imágenes y texto
```

### Caso 3: Migración Gradual desde Claude

**Escenario:** Migración de Claude a Nova sin interrumpir el servicio.

**Estrategia de Migración:**

```python
# config.py - Configuración por etapas
import os

# Fase 1: Prueba con documentos no críticos
CONTEXT_MODEL_MAPPING = {
    'development': 'amazon.nova-micro-v1:0',
    'testing': 'amazon.nova-lite-v1:0', 
    'production': 'anthropic.claude-3-5-sonnet-20240620-v1:0'
}

environment = os.getenv('ENVIRONMENT', 'development')
model_id = CONTEXT_MODEL_MAPPING[environment]

os.environ['BEDROCK_CONTEXT_MODEL_ID'] = model_id
```

## Comparación de Costos

### Análisis de Costo por 1M de Tokens (Aproximado)

| Modelo | Costo Relativo | Uso Recomendado |
|--------|----------------|-----------------|
| Nova Micro | 1x (baseline) | Contexto básico, alta frecuencia |
| Nova Lite | 2-3x | Contenido multimodal, velocidad |
| Nova Pro | 4-6x | Análisis complejo, alta calidad |
| Claude 3.5 Sonnet | 8-10x | Tareas críticas, máxima calidad |

### Ejemplo de Ahorro de Costos

```python
# Cálculo de ahorro usando Nova Micro vs Claude
def calculate_cost_savings():
    monthly_context_requests = 100000  # 100K requests/mes
    avg_tokens_per_request = 200
    
    # Costos aproximados por 1K tokens
    claude_cost_per_1k = 0.003  # $3 por 1M tokens
    nova_micro_cost_per_1k = 0.0004  # $0.4 por 1M tokens
    
    total_tokens_monthly = (monthly_context_requests * avg_tokens_per_request) / 1000
    
    claude_monthly_cost = total_tokens_monthly * claude_cost_per_1k
    nova_monthly_cost = total_tokens_monthly * nova_micro_cost_per_1k
    
    savings = claude_monthly_cost - nova_monthly_cost
    savings_percentage = (savings / claude_monthly_cost) * 100
    
    print(f"Costo mensual con Claude: ${claude_monthly_cost:.2f}")
    print(f"Costo mensual con Nova Micro: ${nova_monthly_cost:.2f}")
    print(f"Ahorro mensual: ${savings:.2f} ({savings_percentage:.1f}%)")

calculate_cost_savings()
# Output esperado:
# Costo mensual con Claude: $60.00
# Costo mensual con Nova Micro: $8.00
# Ahorro mensual: $52.00 (86.7%)
```

## Migración desde Claude

### Checklist de Migración

1. **Preparación:**
   ```bash
   # Backup de configuración actual
   cp .env .env.claude.backup
   ```

2. **Configuración Nova:**
   ```bash
   # Actualizar variables de entorno
   CONTEXT_PROVIDER="bedrock"
   BEDROCK_CONTEXT_MODEL_ID="amazon.nova-micro-v1:0"
   ```

3. **Pruebas A/B:**
   ```python
   # Script de comparación de calidad
   import os
   from providers.aws_bedrock import invoke_bedrock_model
   
   def compare_models(prompt):
       models = [
           "anthropic.claude-3-5-sonnet-20240620-v1:0",
           "amazon.nova-micro-v1:0",
           "amazon.nova-lite-v1:0"
       ]
       
       results = {}
       for model in models:
           result = invoke_bedrock_model(
               model_id=model,
               prompt=prompt,
               max_tokens=200,
               temperature=0.5
           )
           results[model] = result
       
       return results
   
   # Usar para evaluar calidad en tu contenido específico
   ```

4. **Monitoreo Post-Migración:**
   ```python
   # Métricas a monitorear
   metrics = {
       'response_time': [],
       'token_usage': [],
       'context_quality_score': [],
       'cost_per_request': []
   }
   ```

## Troubleshooting

### Problemas Comunes y Soluciones

#### 1. Error: "Model not available in region"

```python
# Solución: Verificar disponibilidad regional
SUPPORTED_REGIONS = [
    'us-east-1',
    'us-west-2', 
    'eu-west-1'
]

# Usar región soportada
os.environ['AWS_REGION'] = 'us-east-1'
```

#### 2. Error: "Access Denied"

```bash
# Verificar permisos IAM
aws iam list-attached-role-policies --role-name YourBedrockRole

# Política mínima requerida:
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel"
            ],
            "Resource": [
                "arn:aws:bedrock:*::foundation-model/amazon.nova-*"
            ]
        }
    ]
}
```

#### 3. Respuestas de Baja Calidad

```python
# Ajustar parámetros para mejor calidad
optimized_params = {
    'max_tokens': 300,      # Más tokens para respuestas completas
    'temperature': 0.3,     # Menos aleatoriedad
    'top_p': 0.8           # Más enfoque
}
```

#### 4. Latencia Alta

```python
# Optimizaciones para latencia
def optimize_for_speed():
    return {
        'model_id': 'amazon.nova-micro-v1:0',  # Modelo más rápido
        'max_tokens': 150,                      # Limitar tokens
        'temperature': 0.1,                     # Mínima aleatoriedad
        'region': 'us-east-1'                   # Región más cercana
    }
```

## Scripts de Utilidad

### Script de Prueba de Rendimiento

```python
#!/usr/bin/env python3
# performance_test.py

import time
import statistics
from providers.aws_bedrock import invoke_bedrock_model

def performance_test(model_id, test_prompts, iterations=5):
    """Prueba de rendimiento para modelos Nova."""
    results = {
        'response_times': [],
        'token_counts': [],
        'success_rate': 0
    }
    
    successful_requests = 0
    
    for i in range(iterations):
        for prompt in test_prompts:
            start_time = time.time()
            
            try:
                response = invoke_bedrock_model(
                    model_id=model_id,
                    prompt=prompt,
                    max_tokens=200,
                    temperature=0.5
                )
                
                end_time = time.time()
                response_time = end_time - start_time
                
                if response:
                    results['response_times'].append(response_time)
                    results['token_counts'].append(len(response.split()))
                    successful_requests += 1
                    
            except Exception as e:
                print(f"Error en iteración {i}: {e}")
    
    total_requests = iterations * len(test_prompts)
    results['success_rate'] = (successful_requests / total_requests) * 100
    
    if results['response_times']:
        print(f"\n=== Resultados para {model_id} ===")
        print(f"Tiempo promedio de respuesta: {statistics.mean(results['response_times']):.2f}s")
        print(f"Mediana de tiempo: {statistics.median(results['response_times']):.2f}s")
        print(f"Tokens promedio: {statistics.mean(results['token_counts']):.1f}")
        print(f"Tasa de éxito: {results['success_rate']:.1f}%")
    
    return results

# Ejemplo de uso
if __name__ == "__main__":
    test_prompts = [
        "Resume este documento en una oración:",
        "Extrae las palabras clave principales:",
        "Proporciona contexto para búsqueda semántica:"
    ]
    
    models_to_test = [
        "amazon.nova-micro-v1:0",
        "amazon.nova-lite-v1:0"
    ]
    
    for model in models_to_test:
        performance_test(model, test_prompts)
```

### Script de Monitoreo de Costos

```python
#!/usr/bin/env python3
# cost_monitor.py

import boto3
import json
from datetime import datetime, timedelta

def get_bedrock_costs(days_back=7):
    """Monitorea costos de Bedrock por modelo."""
    client = boto3.client('ce')  # Cost Explorer
    
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days_back)
    
    response = client.get_cost_and_usage(
        TimePeriod={
            'Start': start_date.strftime('%Y-%m-%d'),
            'End': end_date.strftime('%Y-%m-%d')
        },
        Granularity='DAILY',
        Metrics=['BlendedCost'],
        GroupBy=[
            {'Type': 'DIMENSION', 'Key': 'SERVICE'},
        ],
        Filter={
            'Dimensions': {
                'Key': 'SERVICE',
                'Values': ['Amazon Bedrock']
            }
        }
    )
    
    return response

# Ejemplo de uso
if __name__ == "__main__":
    costs = get_bedrock_costs()
    print(json.dumps(costs, indent=2, default=str))
```

## Conclusión

Los modelos Amazon Nova ofrecen una excelente alternativa para reducir costos manteniendo funcionalidad RAG efectiva. La elección del modelo depende de tus necesidades específicas:

- **Nova Micro**: Para máximo ahorro de costos en tareas simples
- **Nova Lite**: Para contenido multimodal con velocidad
- **Nova Pro**: Para análisis complejo con calidad premium

La migración es sencilla y los beneficios en costos pueden ser significativos, especialmente para aplicaciones con alto volumen de procesamiento de contexto.
