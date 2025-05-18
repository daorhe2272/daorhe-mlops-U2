import os
import pytest

from funcion import app
from fastapi.testclient import TestClient

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_and_teardown():
    # Configuración: Limpiar archivo de predicciones antes de cada prueba
    if os.path.exists('predicciones.json'):
        os.remove('predicciones.json')
    yield
    # Limpieza: Eliminar archivo de predicciones después de cada prueba
    if os.path.exists('predicciones.json'):
        os.remove('predicciones.json')

def test_initial_statistics_empty():
    """Verifica que las estadísticas iniciales estén vacías"""
    response = client.get("/reporte")
    assert response.status_code == 200
    data = response.json()
    assert data["total_predicciones"] == 0
    assert data["predicciones_por_categoria"] == {}
    assert data["ultimas_predicciones"] == []
    assert data["fecha_ultima_prediccion"] is None
    assert "No hay predicciones registradas" in data["mensaje"]

@pytest.mark.parametrize("test_input,expected", [
    # Caso NO ENFERMO
    ({
        "edad": 35,
        "presion_sistolica": 120,
        "presion_diastolica": 80,
        "frecuencia_cardiaca": 75,
        "temperatura": 36.5,
        "duracion_sintomas": 2,
        "tiene_alergias": False,
        "medicacion_previa": False,
        "nivel_dolor": 2
    }, "NO ENFERMO"),
    
    # Caso ENFERMEDAD LEVE
    ({
        "edad": 45,
        "presion_sistolica": 135,
        "presion_diastolica": 85,
        "frecuencia_cardiaca": 90,
        "temperatura": 37.2,
        "duracion_sintomas": 5,
        "tiene_alergias": True,
        "medicacion_previa": True,
        "nivel_dolor": 4
    }, "ENFERMEDAD LEVE"),
    
    # Caso ENFERMEDAD AGUDA
    ({
        "edad": 50,
        "presion_sistolica": 145,
        "presion_diastolica": 95,
        "frecuencia_cardiaca": 110,
        "temperatura": 38.5,
        "duracion_sintomas": 3,
        "tiene_alergias": True,
        "medicacion_previa": True,
        "nivel_dolor": 5
    }, "ENFERMEDAD AGUDA"),
    
    # Caso ENFERMEDAD CRÓNICA
    ({
        "edad": 70,
        "presion_sistolica": 160,
        "presion_diastolica": 100,
        "frecuencia_cardiaca": 95,
        "temperatura": 37.8,
        "duracion_sintomas": 30,
        "tiene_alergias": True,
        "medicacion_previa": True,
        "nivel_dolor": 8
    }, "ENFERMEDAD CRÓNICA"),
    
    # Caso ENFERMEDAD TERMINAL
    ({
        "edad": 85,
        "presion_sistolica": 185,
        "presion_diastolica": 115,
        "frecuencia_cardiaca": 155,
        "temperatura": 39.8,
        "duracion_sintomas": 35,
        "tiene_alergias": True,
        "medicacion_previa": True,
        "nivel_dolor": 9
    }, "ENFERMEDAD TERMINAL")
])
def test_prediction_categories(test_input, expected):
    """Verifica que las predicciones retornen las categorías esperadas para diferentes casos de entrada"""
    response = client.post("/predecir", json=test_input)
    assert response.status_code == 200
    assert response.json()["estado_predicho"] == expected

def test_statistics_after_prediction():
    """Verifica que las estadísticas se actualicen correctamente después de realizar una predicción"""
    # Realizar una predicción
    test_input = {
        "edad": 35,
        "presion_sistolica": 120,
        "presion_diastolica": 80,
        "frecuencia_cardiaca": 75,
        "temperatura": 36.5,
        "duracion_sintomas": 2,
        "tiene_alergias": False,
        "medicacion_previa": False,
        "nivel_dolor": 2
    }
    
    # Realizar la predicción
    prediction_response = client.post("/predecir", json=test_input)
    assert prediction_response.status_code == 200
    predicted_category = prediction_response.json()["estado_predicho"]
    
    # Verificar estadísticas
    stats_response = client.get("/reporte")
    assert stats_response.status_code == 200
    stats = stats_response.json()
    
    # Verificar estadísticas
    assert stats["total_predicciones"] == 1
    assert stats["predicciones_por_categoria"][predicted_category] == 1
    assert len(stats["ultimas_predicciones"]) == 1
    assert stats["ultimas_predicciones"][0]["prediccion"] == predicted_category
    assert stats["mensaje"] is None
    
    # Verificar que la última predicción coincida con nuestros datos de entrada
    last_prediction = stats["ultimas_predicciones"][0]
    assert last_prediction["edad"] == test_input["edad"]
    assert last_prediction["presion_sistolica"] == test_input["presion_sistolica"]
    assert last_prediction["presion_diastolica"] == test_input["presion_diastolica"]
    assert last_prediction["frecuencia_cardiaca"] == test_input["frecuencia_cardiaca"]
    assert last_prediction["temperatura"] == test_input["temperatura"]
    assert last_prediction["duracion_sintomas"] == test_input["duracion_sintomas"]
    assert last_prediction["tiene_alergias"] == test_input["tiene_alergias"]
    assert last_prediction["medicacion_previa"] == test_input["medicacion_previa"]
    assert last_prediction["nivel_dolor"] == test_input["nivel_dolor"] 