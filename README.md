# Servicio de Predicción de Estado de Salud

## Problema

La identificación temprana de enfermedades, especialmente aquellas raras o huérfanas, es un desafío crítico en el sector de la salud. Los diagnósticos tardíos pueden llevar a un empeoramiento de la condición del paciente y a la pérdida de oportunidades para intervenciones efectivas. Los síntomas son a menudo subjetivos, inconsistentes o incluso contradictorios, lo que dificulta un diagnóstico preciso y oportuno.

## Finalidad

Este programa de software proporciona una API simple que predice el estado de salud de un paciente basado en múltiples parámetros médicos relevantes.

Los posibles estados retornados por el servicio son:
*   `NO ENFERMO`
*   `ENFERMEDAD LEVE`
*   `ENFERMEDAD AGUDA`
*   `ENFERMEDAD CRÓNICA`

## Estructura del Repositorio

Este repositorio contiene una API de servicio de predicción de estado de salud implementada con FastAPI. A continuación se describe la estructura y propósito de cada archivo:

## Archivos Principales

- `funcion.py`: Contiene la implementación principal de la API, incluyendo:
  - Definición de modelos de datos (SintomasInput, PrediccionOutput)
  - Lógica de predicción simulada
  - Endpoints de la API (/predecir y /)
  - Validación de datos de entrada

- `Dockerfile`: Configuración para containerizar la aplicación:
  - Basado en Python 3.9-slim
  - Instala las dependencias necesarias
  - Expone el puerto 5000
  - Configura el comando de inicio con uvicorn

- `requirements.txt`: Lista de dependencias del proyecto:
  - fastapi: Framework web para la API
  - uvicorn: Servidor ASGI para ejecutar la aplicación
  - pydantic: Biblioteca para validación de datos

## Características del Proyecto

- API RESTful con FastAPI
- Validación de datos con Pydantic
- Documentación automática de la API (disponible en /docs)
- Containerización con Docker
- Simulación de predicción de estado de salud basada en múltiples parámetros médicos

## Endpoints Disponibles

- `POST /predecir`: Endpoint principal para obtener predicciones
- `GET /`: Endpoint de verificación de estado del servicio

## Requisitos del Sistema

- Python 3.9 o superior
- Docker (opcional, para ejecución en contenedor)
- Dependencias listadas en requirements.txt
