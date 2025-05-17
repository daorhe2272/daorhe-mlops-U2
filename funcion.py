from typing import List
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException


app = FastAPI(
    title="Servicio de Predicción de Estado de Salud (Simulado)",
    description="API simple para obtener una predicción simulada del estado de salud basada en 3 valores de entrada.",
    version="1.0.0"
)

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


class PrediccionOutput(BaseModel):
    estado_predicho: str = Field(..., description="El estado de salud predicho basado en los valores de entrada")


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

# --- Endpoint de la API ---
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
        return {"estado_predicho": resultado}
    except Exception as e:
        # Captura errores inesperados en la lógica de simulación
        raise HTTPException(status_code=500, detail=f"Error interno al procesar la predicción: {str(e)}")


# --- OPCIONAL: Endpoint Raíz para verificar que el servicio está en línea ---
@app.get("/", tags=["General"])
async def root():
    """ Mensaje de bienvenida y estado del servicio. """
    return {"mensaje": "Bienvenido al Servicio de Predicción Simulada. Use el endpoint /predecir (POST) para obtener resultados."}