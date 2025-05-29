# Pipeline de Machine Learning para la Detección Temprana de Enfermedades Huérfanas

## Descripción del Proyecto

Este proyecto implementa un pipeline completo de Machine Learning (ML) diseñado específicamente para asistir a profesionales de la salud en la detección temprana de **Enfermedades Huérfanas (EHs)** o enfermedades raras. El sistema utiliza síntomas, datos demográficos y clínicos del paciente para predecir la posible presencia de una enfermedad huérfana, con el objetivo de reducir el tiempo de diagnóstico y mejorar los resultados clínicos.

### Problema que Resuelve

Las enfermedades huérfanas afectan a un número reducido de personas pero representan un desafío significativo para la salud pública. El principal problema es el **diagnóstico tardío**, que puede tomar años y someter a pacientes y familias a una "odisea diagnóstica" con considerable sufrimiento y empeoramiento del pronóstico.

### Objetivos

- **Reducir el tiempo de diagnóstico** de enfermedades huérfanas
- **Facilitar derivaciones más certeras** a especialistas apropiados
- **Servir como herramienta de apoyo** a la decisión clínica (no como sustituto del juicio médico)
- **Mejorar la calidad de vida** de los pacientes afectados

## Características Principales

### Datos de Entrada Estandarizados
- **Síntomas estructurados** usando ontología **SNOMED CT**
- **Mapeo automático** de texto libre a códigos SNOMED CT con **MedCAT**
- **Datos demográficos detallados** (edad en años/meses para pediatría, género)
- **Datos clínicos adicionales** (peso, altura, historial familiar de EHs)

### Salida Detallada y Accionable
- **Clasificación por niveles de sospecha** de enfermedad huérfana
- **Lista de EHs candidatas** con probabilidades asociadas
- **Puntuación de confianza** para cada predicción
- **Explicaciones interpretables (XAI)** usando SHAP
- **Recomendaciones de derivación** y estudios adicionales

## Tecnologías Implementadas

### Fase de Desarrollo
- **Orquestación de datos**: Apache Airflow
- **Procesamiento**: Pandas, Dask para datasets grandes
- **Versionamiento**: DVC (Data Version Control)
- **Balanceo de datos**: SMOTE (imbalanced-learn)
- **Feature Store**: Feast
- **Anonimización**: ARX De-Identification Tool

### Modelos de ML
- **XGBoost**: Para rendimiento en datos tabulares
- **Random Forest**: Para robustez y interpretabilidad
- **MLP (TensorFlow/Keras)**: Para patrones no lineales complejos
- **Seguimiento de experimentos**: MLflow Tracking
- **Explicabilidad**: SHAP (SHapley Additive exPlanations)

### Infraestructura de Producción
- **API de servicio**: FastAPI desplegado en Kubernetes (Amazon EKS)
- **Contenedorización**: Docker
- **Registro de modelos**: MLflow Model Registry
- **Interfaz de usuario**: Streamlit para desarrollo rápido
- **Monitorización**: Evidently AI, Prometheus, Grafana
- **CI/CD/CT**: GitHub Actions con despliegues Canary/Blue-Green

## Arquitectura del Pipeline

### Fase 1: Diseño y Planificación Estratégica
- Definición de objetivos y KPIs específicos para EHs
- Estandarización de datos de entrada con SNOMED CT
- Diseño de salidas accionables con explicabilidad
- Estrategias de mitigación de sesgos y limitaciones éticas

### Fase 2: Desarrollo Táctica y Operativa
- **Fuentes de datos**: EHRs vía HL7 FHIR, Orphanet, OMIM
- **NLP especializado**: BioBERT/SciBERT para literatura médica
- **Pipeline de datos robusto** con validación y versionamiento
- **Experimentación rigurosa** con validación cruzada estratificada
- **Pruebas de sesgo** con Aequitas, IBM AI Fairness 360

### Fase 3: Producción y MLOps
- **Despliegue escalable** en Kubernetes con auto-scaling
- **Monitorización continua** de deriva de datos y rendimiento
- **Reentrenamiento automatizado** con validación exhaustiva
- **Gobernanza del modelo** con auditorías y documentación

## KPIs y Métricas

### Indicadores Primarios
- **Reducción del tiempo promedio de diagnóstico** para EHs identificadas
- **Tasa de derivación correcta** (pacientes con sospecha confirmada)
- **Sensibilidad (Recall) para EHs**: Maximizar detección de EHs reales
- **Valor Predictivo Positivo (VPP)** para EHs

### Indicadores Secundarios
- **Tasa de adopción** por profesionales de la salud
- **Satisfacción del usuario** (médicos)

## Ejemplo de Uso

### Datos de Entrada (JSON)
```json
{
  "paciente_id": "P00123",
  "edad_años": 7,
  "genero": "Masculino",
  "sintomas_snomed": [
    {
      "codigo_snomed": "271807003",
      "termino": "Dolor abdominal"
    },
    {
      "codigo_snomed": "386661006",
      "termino": "Fiebre"
    },
    {
      "codigo_snomed": "422587007",
      "termino": "Vómitos"
    },
    {
      "codigo_snomed": "267036007",
      "termino": "Pérdida de peso involuntaria"
    }
  ],
  "historial_familiar_EH": false
}
```

### Datos de Salida (JSON)
```json
{
  "paciente_id": "P00123",
  "prediccion_general": "Alta sospecha de Enfermedad Huérfana",
  "posibles_EHs_sugeridas": [
    {
      "nombre_EH": "Enfermedad Inflamatoria Intestinal de Inicio Muy Temprano",
      "probabilidad_estimada": 0.75,
      "cod_orphanet": "ORPHA:280471"
    },
    {
      "nombre_EH": "Fibrosis Quística (forma atípica)",
      "probabilidad_estimada": 0.15,
      "cod_orphanet": "ORPHA:586"
    }
  ],
  "puntuacion_confianza_general": 0.82,
  "factores_contribuyentes_XAI": [
    "Pérdida de peso involuntaria",
    "Dolor abdominal (crónico)",
    "Edad de inicio temprana"
  ],
  "recomendacion": "Considerar derivación a gastroenterología pediátrica y pruebas genéticas específicas."
}
```

## Instalación y Configuración

### Prerrequisitos
- Python 3.9+
- Docker y Docker Compose
- Kubernetes (para producción)
- AWS CLI (para servicios cloud)

## Desarrollo y Contribución

### Estructura del Proyecto
```
├── src/
│   ├── data/              # Scripts de ingesta y procesamiento
│   ├── models/            # Definición y entrenamiento de modelos
│   ├── api/               # Código de la API FastAPI
│   └── utils/             # Utilidades compartidas
├── data/
│   ├── raw/               # Datos crudos
│   ├── processed/         # Datos procesados
│   └── external/          # Datos externos (Orphanet, OMIM)
├── models/                # Modelos entrenados
├── notebooks/             # Jupyter notebooks para exploración
├── tests/                 # Pruebas unitarias e integración
├── docker/                # Archivos Docker
├── k8s/                   # Manifiestos Kubernetes
└── docs/                  # Documentación adicional
```

### Flujo de Desarrollo

1. **Desarrollo de características**:
```bash
git checkout -b feature/nueva-caracteristica
# Desarrollar y testear
pytest tests/
```

2. **Pipeline CI/CD**:
- Commit dispara GitHub Actions
- Pruebas automatizadas con pytest
- Entrenamiento con MLflow
- Validación de modelos
- Despliegue automático si las pruebas pasan

3. **Monitorización**:
- Métricas operacionales en Grafana
- Deriva de datos con Evidently AI
- Alertas automáticas por Prometheus

## Pipeline CI/CD/CT Detallado

### Disparadores (Triggers)
- Commits a la rama principal en GitHub
- Nuevas etiquetas de versión de datos en DVC
- Alertas de monitorización (Prometheus/Evidently)

### Flujo Automatizado
1. **CI (GitHub Actions):**
   - Clonación de código y obtención de datos de DVC
   - Pruebas unitarias y de integración

2. **CT (Continuous Training):**
   - Entrenamiento de modelos candidatos (XGBoost, RF, MLP) con MLflow
   - Evaluación contra "ML Test Score System"
   - Generación de reportes XAI con SHAP

3. **CD (Continuous Deployment):**
   - Registro en MLflow Model Registry
   - Construcción de imagen Docker
   - Despliegue en Kubernetes (EKS) con estrategias Canary/Blue-Green usando Argo Rollouts

## Consideraciones Éticas y Legales

### Privacidad y Seguridad
- **Cumplimiento GDPR/HIPAA**: Anonimización robusta con ARX
- **Cifrado**: Datos en reposo y en tránsito
- **Control de acceso**: RBAC (Role-Based Access Control)
- **Auditorías**: Logs detallados de acceso y uso

### Sesgos y Equidad
- **Pruebas de sesgo** regulares con Aequitas, IBM AI Fairness 360, Fairlearn
- **Análisis de equidad** por grupos demográficos
- **Monitorización continua** de resultados por subpoblaciones

### Responsabilidad Médica
- **Herramienta de apoyo**: No sustituye el juicio clínico
- **Transparencia**: Explicaciones XAI para cada predicción
- **Validación clínica**: Colaboración continua con profesionales médicos

## Monitorización y Mantenimiento

### Monitorización del Modelo
- **Deriva de datos/concepto**: Evidently AI
- **Métricas operacionales**: Prometheus y Grafana
- **Sistema de alertas**: Prometheus Alertmanager

### Reentrenamiento
- **Estrategia híbrida**: Reentrenamiento mensual en batch o por disparadores
- **Validación exhaustiva**: Cada nueva versión se valida completamente antes de producción
- **Rollback automático**: En caso de degradación del rendimiento

### Gobernanza del Modelo
- **Documentación exhaustiva**: Modelos, datos, procesos, decisiones
- **Auditorías periódicas**: Cumplimiento normativo, ético y de rendimiento
- **Gestión del ciclo de vida**: Políticas para retiro y archivo de modelos

## Soporte y Documentación

### Documentación Adicional
- [PIPELINE.md](PIPELINE.md): Descripción detallada del pipeline completo
- [CHANGELOG.md](CHANGELOG.md): Historial de cambios y versiones
- `/docs/api/`: Documentación técnica de la API
- `/docs/models/`: Documentación de modelos y métricas

## Versiones

**Versión Actual**: 1.0.0 - Pipeline Detallado para Detección de Enfermedades Raras

### Historial de Versiones
- **v1.0.0 (2025-05-28)**: Pipeline completo para detección de EHs con MLOps avanzado
- **v0.1.0**: Esquema inicial del pipeline general de predicción de enfermedades

Ver [CHANGELOG.md](CHANGELOG.md) para el historial completo de cambios y evolución del proyecto.

---

## Estado del Proyecto

Este README refleja la **versión 1.0.0** del pipeline, que representa una evolución significativa desde la versión inicial 0.1.0. El proyecto ha evolucionado de un sistema básico de predicción de enfermedades a un pipeline especializado y completo para la detección de enfermedades huérfanas, incorporando las mejores prácticas de MLOps y herramientas específicas del estado del arte.

Para obtener información sobre las implementaciones actuales y el estado de desarrollo, consulte los archivos adjuntos del proyecto y la documentación técnica detallada. 