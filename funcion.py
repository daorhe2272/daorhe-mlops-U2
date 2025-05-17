import os
import json
import pytz

from datetime import datetime
from collections import Counter
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from fastapi import FastAPI, HTTPException

# Configuración de la API
app = FastAPI(
    title="Servicio de Predicción de Estado de Salud (Simulado)",
    description="API simple para obtener una predicción simulada del estado de salud basada en 3 valores de entrada.",
    version="1.0.0"
)

# Modelo de entrada para los síntomas del paciente
class SintomasInput(BaseModel):
    edad: int = Field(..., description="Edad del paciente en años", ge=0, le=120)
    presion_sistolica: int = Field(..., description="Presión arterial sistólica (mmHg)", ge=60, le=250)
    presion_diastolica: int = Field(..., description="Presión arterial diastólica (mmHg)", ge=40, le=150)
    frecuencia_cardiaca: int = Field(..., description="Frecuencia cardíaca (latidos por minuto)", ge=40, le=200)
    temperatura: float = Field(..., description="Temperatura corporal (°C)", ge=35.0, le=42.0)
    duracion_sintomas: int = Field(..., description="Duración de los síntomas en días", ge=0, le=365)
    tiene_alergias: bool = Field(..., description="Indica si el paciente tiene alergias conocidas")
    medicacion_previa: bool = Field(..., description="Indica si el paciente está tomando medicación")
    nivel_dolor: int = Field(..., description="Nivel de dolor reportado (escala 0-10)", ge=0, le=10)

# Modelo de salida para la predicción del estado de salud
class PrediccionOutput(BaseModel):
    estado_predicho: str = Field(..., description="El estado de salud predicho basado en los valores de entrada")

# Modelo de salida para el reporte de estadísticas de predicciones
class UltimaPrediccion(BaseModel):
    fecha_hora: str
    edad: int
    presion_sistolica: int
    presion_diastolica: int
    frecuencia_cardiaca: int
    temperatura: float
    duracion_sintomas: int
    tiene_alergias: bool
    medicacion_previa: bool
    nivel_dolor: int
    prediccion: str

# Modelo de salida para el reporte de estadísticas de predicciones  
class ReporteOutput(BaseModel):
    total_predicciones: int = Field(..., description="Número total de predicciones realizadas")
    predicciones_por_categoria: Dict[str, int] = Field(..., description="Conteo de predicciones por cada categoría")
    ultimas_predicciones: List[UltimaPrediccion] = Field(..., description="Las últimas 5 predicciones realizadas")
    fecha_ultima_prediccion: Optional[str] = Field(None, description="Fecha y hora de la última predicción")
    mensaje: Optional[str] = Field(None, description="Mensaje informativo cuando no hay predicciones")

def simular_prediccion(datos: SintomasInput) -> str:
    """
    Simula la predicción de un estado de salud basado en múltiples factores médicos.
    Esta es una versión simplificada que será reemplazada por un modelo de Deep Learning.
    """
    # Verificación de factores de riesgo críticos
    factores_criticos = (
        datos.edad > 80 and
        (datos.presion_sistolica > 180 or datos.presion_diastolica > 110) and
        (datos.frecuencia_cardiaca > 150 or datos.frecuencia_cardiaca < 40) and
        datos.temperatura > 39.5 and
        datos.nivel_dolor > 8 and
        datos.duracion_sintomas > 30
    )
    
    if factores_criticos:
        return "ENFERMEDAD TERMINAL"

    # Factores de riesgo calculados
    riesgo_edad = 1 if datos.edad > 65 else 0
    riesgo_presion = 1 if (datos.presion_sistolica > 140 or datos.presion_diastolica > 90) else 0
    riesgo_frecuencia = 1 if (datos.frecuencia_cardiaca > 100 or datos.frecuencia_cardiaca < 60) else 0
    riesgo_temperatura = 1 if datos.temperatura > 37.5 else 0
    riesgo_duracion = 1 if datos.duracion_sintomas > 7 else 0
    
    # Puntuación total de riesgo
    puntuacion_riesgo = (
        riesgo_edad +
        riesgo_presion +
        riesgo_frecuencia +
        riesgo_temperatura +
        riesgo_duracion +
        (1 if datos.tiene_alergias else 0) +
        (1 if datos.medicacion_previa else 0) +
        (datos.nivel_dolor // 3)  # Convierte el nivel de dolor a un factor de riesgo
    )

    if puntuacion_riesgo <= 2:
        return "NO ENFERMO"
    elif puntuacion_riesgo <= 4:
        return "ENFERMEDAD LEVE"
    elif puntuacion_riesgo <= 6:
        return "ENFERMEDAD AGUDA"
    else:
        return "ENFERMEDAD CRÓNICA"

def log_prediccion(sintomas: SintomasInput, prediccion: str):
    """
    Registra una predicción en el archivo JSON de predicciones con la fecha y hora local de Bogotá.
    
    Args:
        sintomas (SintomasInput): Objeto que contiene todos los síntomas y datos del paciente
        prediccion (str): El resultado de la predicción del estado de salud
        
    El archivo JSON almacena un array de objetos, donde cada objeto contiene:
        - fecha_hora: Timestamp en formato YYYY-MM-DD HH:MM:SS (hora de Bogotá)
        - edad: Edad del paciente en años
        - presion_sistolica: Presión arterial sistólica en mmHg
        - presion_diastolica: Presión arterial diastólica en mmHg
        - frecuencia_cardiaca: Frecuencia cardíaca en latidos por minuto
        - temperatura: Temperatura corporal en °C
        - duracion_sintomas: Duración de los síntomas en días
        - tiene_alergias: Indicador booleano de alergias
        - medicacion_previa: Indicador booleano de medicación previa
        - nivel_dolor: Nivel de dolor reportado (0-10)
        - prediccion: Estado de salud predicho
    """

    # Configuración de la zona horaria de Bogotá
    bogota_tz = pytz.timezone('America/Bogota')
    fecha_hora = datetime.now(bogota_tz).strftime('%Y-%m-%d %H:%M:%S')
    
    # Creación del objeto de predicción
    prediccion_data = {
        'fecha_hora': fecha_hora,
        'edad': sintomas.edad,
        'presion_sistolica': sintomas.presion_sistolica,
        'presion_diastolica': sintomas.presion_diastolica,
        'frecuencia_cardiaca': sintomas.frecuencia_cardiaca,
        'temperatura': sintomas.temperatura,
        'duracion_sintomas': sintomas.duracion_sintomas,
        'tiene_alergias': sintomas.tiene_alergias,
        'medicacion_previa': sintomas.medicacion_previa,
        'nivel_dolor': sintomas.nivel_dolor,
        'prediccion': prediccion
    }
    
    # Lectura del archivo de predicciones si existe
    predicciones = []
    if os.path.exists('predicciones.json'):
        with open('predicciones.json', 'r', encoding='utf-8') as file:
            try:
                predicciones = json.load(file)
            except json.JSONDecodeError:
                predicciones = []
    
    # Agregar la predicción al archivo de predicciones
    predicciones.append(prediccion_data)
    
    # Escritura del archivo de predicciones
    with open('predicciones.json', 'w', encoding='utf-8') as file:
        json.dump(predicciones, file, indent=2, ensure_ascii=False)

def obtener_predicciones() -> List[dict]:
    """
    Lee y retorna las predicciones almacenadas en el archivo JSON.
    Si el archivo no existe o está vacío, retorna una lista vacía.
    """
    if not os.path.exists('predicciones.json'):
        return []
    
    try:
        with open('predicciones.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

# Endpoint para obtener una predicción simulada del estado de salud
@app.post("/predecir",
          response_model=PrediccionOutput,
          summary="Obtiene una predicción simulada del estado de salud",
          tags=["Predicción"])

async def predecir_estado(sintomas: SintomasInput):
    """
    Recibe múltiples parámetros médicos y retorna una predicción simulada:
    - **edad**: Edad del paciente en años
    - **presion_sistolica**: Presión arterial sistólica
    - **presion_diastolica**: Presión arterial diastólica
    - **frecuencia_cardiaca**: Frecuencia cardíaca
    - **temperatura**: Temperatura corporal
    - **duracion_sintomas**: Duración de los síntomas
    - **tiene_alergias**: Indicador de alergias
    - **medicacion_previa**: Indicador de medicación previa
    - **nivel_dolor**: Nivel de dolor reportado

    Retorna uno de los siguientes estados:
    - NO ENFERMO
    - ENFERMEDAD LEVE
    - ENFERMEDAD AGUDA
    - ENFERMEDAD CRÓNICA
    """
    try:
        resultado = simular_prediccion(sintomas)
        log_prediccion(sintomas, resultado)
        return {"estado_predicho": resultado}
    except Exception as e:
        # Captura errores inesperados en la lógica de simulación
        raise HTTPException(status_code=500, detail=f"Error interno al procesar la predicción: {str(e)}")

# Endpoint para obtener estadísticas de las predicciones realizadas
@app.get("/reporte",
         response_model=ReporteOutput,
         summary="Obtiene estadísticas de las predicciones realizadas",
         tags=["Reportes"])

async def generar_reporte():
    """
    Genera un reporte con estadísticas de las predicciones realizadas, incluyendo:
    - Número total de predicciones
    - Conteo de predicciones por categoría
    - Las últimas 5 predicciones
    - Fecha de la última predicción
    
    Si no hay predicciones, retorna un mensaje informativo.
    """
    predicciones = obtener_predicciones()
    
    if not predicciones:
        return {
            "total_predicciones": 0,
            "predicciones_por_categoria": {},
            "ultimas_predicciones": [],
            "fecha_ultima_prediccion": None,
            "mensaje": "No hay predicciones registradas. Genere predicciones usando el endpoint /predecir para ver las estadísticas."
        }
    
    # Ordenar predicciones por fecha (más recientes primero)
    predicciones_ordenadas = sorted(predicciones, 
                                  key=lambda x: x['fecha_hora'], 
                                  reverse=True)
    
    # Contar predicciones por categoría
    categorias = Counter(pred['prediccion'] for pred in predicciones)
    
    return {
        "total_predicciones": len(predicciones),
        "predicciones_por_categoria": dict(categorias),
        "ultimas_predicciones": predicciones_ordenadas[:5],
        "fecha_ultima_prediccion": predicciones_ordenadas[0]['fecha_hora'] if predicciones_ordenadas else None,
        "mensaje": None
    }

# --- OPCIONAL: Endpoint Raíz para verificar que el servicio está en línea ---
@app.get("/", tags=["General"])
async def root():
    """ Mensaje de bienvenida y estado del servicio. """
    return {"mensaje": "Bienvenido al Servicio de Predicción Simulada. Use el endpoint /predecir (POST) para obtener resultados."}