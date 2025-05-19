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
*   `ENFERMEDAD TERMINAL`

## Estructura del Repositorio

Este repositorio contiene una API de servicio de predicción de estado de salud implementada con FastAPI. A continuación se describe la estructura y propósito de cada archivo:

### Archivos Principales

- `funcion.py`: Contiene la implementación principal de la API, incluyendo:
  - Definición de modelos de datos (SintomasInput, PrediccionOutput, ReporteOutput)
  - Lógica de predicción simulada
  - Endpoints de la API (/predecir, /reporte y /)
  - Validación de datos de entrada
  - Sistema de logging de predicciones en JSON

- `Dockerfile`: Configuración para containerizar la aplicación:
  - Basado en Python 3.9-slim
  - Instala las dependencias necesarias
  - Expone el puerto 5000
  - Configura el comando de inicio con uvicorn

- `requirements.txt`: Lista de dependencias del proyecto:
  - fastapi: Framework web para la API
  - uvicorn: Servidor ASGI para ejecutar la aplicación
  - pydantic: Biblioteca para validación de datos
  - pytz: Biblioteca para manejo de zonas horarias

- `.gitignore`: Configuración para excluir archivos del control de versiones:
  - predicciones.json: Archivo de registro de predicciones

### Características del Proyecto

- API RESTful con FastAPI
- Validación de datos con Pydantic
- Documentación automática de la API (disponible en /docs)
- Containerización con Docker
- Simulación de predicción de estado de salud basada en múltiples parámetros médicos
- Sistema de logging de predicciones con fecha y hora local (Bogotá)
- Endpoint de reportes con estadísticas de predicciones

### Endpoints Disponibles

- `POST /predecir`: Endpoint principal para obtener predicciones
- `GET /reporte`: Endpoint para obtener estadísticas de las predicciones realizadas
- `GET /`: Endpoint de verificación de estado del servicio

### Requisitos del Sistema

- Python 3.9 o superior
- Docker (opcional, para ejecución en contenedor)
- Dependencias listadas en requirements.txt

## Cómo ejecutar el servicio localmente:

### Prerrequisitos
*   Tener Docker instalado en su sistema.

### Cómo Construir la Imagen Docker
1.  Asegúrese de tener los siguientes archivos en el mismo directorio:
    *   `funcion.py`
    *   `requirements.txt`
    *   `Dockerfile`
    *   `README.md` (este archivo)
2.  Abra una terminal o línea de comandos en ese directorio.
3.  Ejecute el siguiente comando para construir la imagen Docker. Se le asignará el nombre servicio-prediccion:
    ```docker build -t servicio-prediccion .```

### Cómo Correr la Solución (el Contenedor Docker)
1.  Una vez construida la imagen, ejecute el siguiente comando para iniciar un contenedor basado en ella:
    ```docker run -d -p 5000:5000 --name predictor servicio-prediccion```
    *   `-d`: Corre el contenedor en modo "detached" (en segundo plano).
    *   `-p 5000:5000`: Mapea el puerto 5000 de su máquina local al puerto 5000 dentro del contenedor (donde la API está escuchando).
    *   `--name predictor`: Asigna un nombre fácil de recordar al contenedor en ejecución.
    *   `servicio-prediccion`: Es el nombre de la imagen que construimos previamente.
2.  El servicio estará ahora corriendo y accesible en `http://localhost:5000`.

## Cómo Obtener Respuestas del Modelo (Usar la API)
Puede interactuar con la API de varias maneras (usando herramientas como `curl`, Postman, Insomnia, o mediante programación). Los endpoints disponibles son:

### Endpoint de Predicción (`POST /predecir`)
El endpoint principal es `http://localhost:5000/predecir` y espera una solicitud `POST` con un cuerpo JSON que contenga los siguientes campos:

* `edad`: Edad del paciente en años (0-120)
* `presion_sistolica`: Presión arterial sistólica en mmHg (60-250)
* `presion_diastolica`: Presión arterial diastólica en mmHg (40-150)
* `frecuencia_cardiaca`: Latidos por minuto (40-200)
* `temperatura`: Temperatura corporal en °C (35.0-42.0)
* `duracion_sintomas`: Duración de los síntomas en días (0-365)
* `tiene_alergias`: Booleano indicando si tiene alergias
* `medicacion_previa`: Booleano indicando si toma medicación
* `nivel_dolor`: Nivel de dolor en escala 0-10

### Ejemplo usando `curl`:
Abra una terminal y pruebe los siguientes comandos (ajuste los valores para obtener diferentes resultados):

*   **Para obtener "NO ENFERMO":** (Valores dentro de rangos normales)
    ```bash
    curl -X POST "http://localhost:5000/predecir" \
    -H "Content-Type: application/json" \
    -d '{
        "edad": 35,
        "presion_sistolica": 120,
        "presion_diastolica": 80,
        "frecuencia_cardiaca": 75,
        "temperatura": 36.5,
        "duracion_sintomas": 2,
        "tiene_alergias": false,
        "medicacion_previa": false,
        "nivel_dolor": 2
    }'
    ```
    *Respuesta esperada:* `{"estado_predicho":"NO ENFERMO"}`

*   **Para obtener "ENFERMEDAD LEVE":** (Algunos valores ligeramente alterados)
    ```bash
    curl -X POST "http://localhost:5000/predecir" \
    -H "Content-Type: application/json" \
    -d '{
        "edad": 45,
        "presion_sistolica": 135,
        "presion_diastolica": 85,
        "frecuencia_cardiaca": 90,
        "temperatura": 37.2,
        "duracion_sintomas": 5,
        "tiene_alergias": true,
        "medicacion_previa": true,
        "nivel_dolor": 4
    }'
    ```
    *Respuesta esperada:* `{"estado_predicho":"ENFERMEDAD LEVE"}`

*   **Para obtener "ENFERMEDAD AGUDA":** (Varios valores fuera de rango normal)
    ```bash
    curl -X POST "http://localhost:5000/predecir" \
    -H "Content-Type: application/json" \
    -d '{
        "edad": 50,
        "presion_sistolica": 145,
        "presion_diastolica": 95,
        "frecuencia_cardiaca": 110,
        "temperatura": 38.5,
        "duracion_sintomas": 3,
        "tiene_alergias": true,
        "medicacion_previa": true,
        "nivel_dolor": 5
    }'
    ```
    *Respuesta esperada:* `{"estado_predicho":"ENFERMEDAD AGUDA"}`

*   **Para obtener "ENFERMEDAD CRÓNICA":** (Múltiples factores de riesgo)
    ```bash
    curl -X POST "http://localhost:5000/predecir" \
    -H "Content-Type: application/json" \
    -d '{
        "edad": 70,
        "presion_sistolica": 160,
        "presion_diastolica": 100,
        "frecuencia_cardiaca": 95,
        "temperatura": 37.8,
        "duracion_sintomas": 30,
        "tiene_alergias": true,
        "medicacion_previa": true,
        "nivel_dolor": 8
    }'
    ```
    *Respuesta esperada:* `{"estado_predicho":"ENFERMEDAD CRÓNICA"}`

*   **Para obtener "ENFERMEDAD TERMINAL":** (Factores de riesgo críticos)
    ```bash
    curl -X POST "http://localhost:5000/predecir" \
    -H "Content-Type: application/json" \
    -d '{
        "edad": 85,
        "presion_sistolica": 185,
        "presion_diastolica": 115,
        "frecuencia_cardiaca": 155,
        "temperatura": 39.8,
        "duracion_sintomas": 35,
        "tiene_alergias": true,
        "medicacion_previa": true,
        "nivel_dolor": 9
    }'
    ```
    *Respuesta esperada:* `{"estado_predicho":"ENFERMEDAD TERMINAL"}`

### Endpoint de Reportes (`GET /reporte`)
Este endpoint proporciona estadísticas sobre las predicciones realizadas. No requiere parámetros de entrada.

Ejemplo usando `curl`:
```bash
curl -X GET "http://localhost:5000/reporte"
```

La respuesta incluirá:
- Número total de predicciones realizadas
- Conteo de predicciones por cada categoría
- Las últimas 5 predicciones realizadas
- Fecha de la última predicción

Ejemplo de respuesta:
```json
{
    "total_predicciones": 10,
    "predicciones_por_categoria": {
        "NO ENFERMO": 3,
        "ENFERMEDAD LEVE": 4,
        "ENFERMEDAD AGUDA": 2,
        "ENFERMEDAD CRÓNICA": 1
    },
    "ultimas_predicciones": [
        {
            "fecha_hora": "2024-03-14 15:30:45",
            "edad": 45,
            "presion_sistolica": 120,
            "presion_diastolica": 80,
            "frecuencia_cardiaca": 75,
            "temperatura": 36.5,
            "duracion_sintomas": 2,
            "tiene_alergias": false,
            "medicacion_previa": false,
            "nivel_dolor": 2,
            "prediccion": "NO ENFERMO"
        }
        // ... hasta 5 predicciones más recientes
    ],
    "fecha_ultima_prediccion": "2024-03-14 15:30:45",
    "mensaje": null
}
```

Si no hay predicciones registradas, la respuesta será:
```json
{
    "total_predicciones": 0,
    "predicciones_por_categoria": {},
    "ultimas_predicciones": [],
    "fecha_ultima_prediccion": null,
    "mensaje": "No hay predicciones registradas. Genere predicciones usando el endpoint /predecir para ver las estadísticas."
}
```

### Sistema de Logging
- Todas las predicciones se registran automáticamente en el archivo `predicciones.json`
- El archivo incluye fecha y hora local de Bogotá para cada predicción
- El archivo se excluye del control de versiones (git) para mantener los datos locales
- Las predicciones se mantienen en orden cronológico

Adicionalmente, FastAPI genera automáticamente documentación interactiva (Swagger UI). Abra su navegador web y vaya a: `http://localhost:5000/docs`
Desde allí, puede ver los detalles del endpoint `/predecir`, probarlo directamente introduciendo los valores en la interfaz y ver las respuestas.

## Detener y Eliminar el Contenedor
*   Para detener el contenedor: use el comando ```docker stop predictor```
*   Para eliminar el contenedor (después de detenerlo): use el comando ```docker rm predictor```

## Limpiar la Imagen Docker (Opcional)
Si ya no necesita la imagen Docker, puede eliminarla con el comando ```docker rmi servicio-prediccion```

## Ejecutar las Pruebas Unitarias

El proyecto incluye pruebas unitarias para verificar el correcto funcionamiento del servicio. Las pruebas utilizan pytest y cubren:
- Verificación de predicciones para todas las categorías de enfermedad
- Validación de estadísticas iniciales y después de predicciones
- Verificación de la integridad de los datos almacenados

### Ejecutar las Pruebas

Las pruebas unitarias pueden ejecutarse directamente dentro del contenedor Docker para asegurar que el entorno es idéntico al de producción.

1. Asegúrate de que el contenedor esté corriendo (puedes verificar con `docker ps`).
2. Ejecuta el siguiente comando desde tu terminal:

```bash
docker exec predictor pytest tests/test_prediction.py -v
```

Esto ejecutará todas las pruebas y mostrará el resultado en la consola.

El flag `-v` (verbose) muestra información detallada de cada prueba ejecutada.

### Opciones Adicionales de pytest
*   Para ver la cobertura de código: ```pytest --cov=funcion tests/```
*   Para ejecutar una prueba específica: ```pytest tests/test_prediction.py::nombre_del_test -v```
*   Para ver más detalles de las pruebas fallidas: ```pytest -vv tests/test_prediction.py```
*   Para detener la ejecución en el primer error: ```pytest -x tests/test_prediction.py```

### Estructura de las Pruebas
Las pruebas están organizadas en el archivo `tests/test_prediction.py` y cubren:
1. Verificación del estado inicial (estadísticas vacías)
2. Pruebas de predicción para cada categoría de enfermedad:
   - NO ENFERMO
   - ENFERMEDAD LEVE
   - ENFERMEDAD AGUDA
   - ENFERMEDAD CRÓNICA
   - ENFERMEDAD TERMINAL
3. Verificación de estadísticas después de realizar predicciones
4. Validación de la integridad de los datos almacenados

Cada prueba se ejecuta en un entorno aislado, limpiando automáticamente el archivo de predicciones antes y después de cada prueba.
