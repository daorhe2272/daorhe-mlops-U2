# Changelog (Historial de Cambios)

Todos los cambios notables en el Pipeline de ML para la Predicción de Enfermedades se documentarán en este archivo.
El formato se basa en [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
y este proyecto se adhiere al Versionamiento Semántico.

## [1.0.0] - 2025-05-28 (Nuevo Pipeline Detallado para Detección de Enfermedades Raras)

Esta versión representa una revisión y detallado significativos del pipeline de ML, con un enfoque específico en el diagnóstico de enfermedades raras (Enfermedades Huérfanas - EHs) y la incorporación de mejores prácticas exhaustivas de MLOps y herramientas específicas.

### Añadido

#### General
- **Enfoque Específico:** Se enfoca explícitamente en "Enfermedades Huérfanas (EHs)".
- **Contexto Detallado:** Proporciona antecedentes sobre las EHs y la motivación del proyecto.

#### Fase 1: Diseño y Planificación (Estratégica)
- **Objetivos Refinados:**
    - Añadido: Reducir el tiempo de diagnóstico específicamente para las EHs.
    - Añadido: Servir como una herramienta de *apoyo* a la decisión clínica, no como un sustituto del juicio médico.
- **KPIs Granulares:**
    - KPIs categorizados en "Primarios" (ej., Reducción del tiempo promedio de diagnóstico para EHs identificadas, Aumento de la tasa de derivación correcta, Recall para EHs, Valor Predictivo Positivo para EHs) y "Secundarios" (ej., tasa de adopción, satisfacción del usuario).
- **Entrada de Datos Estandarizada y Enriquecida:**
    - Ontología **SNOMED CT** para la estandarización de síntomas.
    - **MedCAT (Medical Concept Annotation Tool)** para mapear síntomas de texto libre a SNOMED CT.
    - Datos demográficos más específicos (ej., edad en años y meses para pediatría).
    - Inclusión de datos clínicos adicionales: altura, historial familiar detallado para EHs.
- **Salida de Datos Detallada y Accionable:**
    - Categorías de clasificación más matizadas, incluyendo "Alta sospecha de Enfermedad Huérfana" con una lista de posibles EHs candidatas y sus probabilidades/puntuaciones asociadas.
    - La salida incluye "Urgencia / Requiere atención especializada inmediata."
    - **Puntuación de confianza** para cada predicción y categoría.
    - **Explicación de la predicción (XAI - Explainable AI)** indicando los síntomas/factores clave contribuyentes.
    - **Ejemplos JSON simplificados** para estructuras de datos de entrada y salida.
- **Estrategias de Mitigación para Limitaciones:**
    - Para la subjetividad de los síntomas: guías claras para la entrada de datos y estandarización ontológica.
    - Para los sesgos en los datos: reconocimiento y consideración en el desarrollo y monitoreo del modelo.

#### Fase 2: Desarrollo (Táctica y Operativa)
- **Adquisición y Fuentes de Datos Específicas:**
    - Estándar **HL7 FHIR (Fast Healthcare Interoperability Resources)** para la integración de EHRs/HCEs.
    - Bases de datos especializadas en EHs: **Orphanet, OMIM**.
    - NLP para minería de literatura: **BioBERT o SciBERT** para extraer relaciones síntoma-enfermedad.
    - Data Lake: **AWS S3** para almacenamiento de datos crudos con justificación.
- **Herramientas/Técnicas Avanzadas de Gestión y Preprocesamiento de Datos:**
    - Orquestación: **Apache Airflow** para la gestión del pipeline de datos.
    - Procesamiento de grandes datasets: **Dask** (junto con Pandas).
    - Anonimización/Pseudonimización Robusta: **ARX De-Identification Tool**.
    - Versionamiento de Datos: **DVC (Data Version Control)** con justificación.
    - Manejo de Datos Desbalanceados: **SMOTE (Synthetic Minority Over-sampling Technique)** de la librería `imbalanced-learn`.
    - Feature Store: **Feast** para gestionar y servir características de ML.
- **Experimentación, Seguimiento y Explicabilidad de ML:**
    - Modelos candidatos iniciales explícitos: **XGBoost, Random Forest, MLP simple (TensorFlow/Keras)** con justificaciones.
    - Plataforma de Seguimiento de Experimentos: **MLflow Tracking**.
    - Marco XAI: **SHAP (SHapley Additive exPlanations)** para la interpretabilidad del modelo.
- **Validación y Pruebas Rigurosas y Estructuradas:**
    - **Conjunto de Prueba (Hold-out Test Set)** para una estimación insesgada del rendimiento final del modelo.
    - **Sistema de Puntuación de Pruebas de ML / Marco de Evaluación de Modelos** para una evaluación consistente y objetiva del modelo a través de versiones y segmentos.
    - Herramientas Específicas para Pruebas de Sesgo: **Aequitas, IBM AI Fairness 360, Fairlearn**.
    - **Pruebas de Robustez** contra pequeñas perturbaciones en los datos de entrada o datos fuera de la distribución de entrenamiento.
    - Análisis detallado de errores enfocado en EHs.

#### Fase 3: Producción y Operacionalización (MLOps)
- **Infraestructura Sofisticada de Despliegue y Servicio:**
    - Servicio del Modelo (Model Serving): Framework **FastAPI** desplegado en **Kubernetes (específicamente Amazon EKS - Elastic Kubernetes Service)**.
    - **Arquitectura Modular y Débilmente Acoplada** para los componentes del sistema.
    - Registro de Modelos: **MLflow Model Registry** para versionar y gestionar modelos en producción.
    - Interfaz de Usuario Inicial (Front-End): **Streamlit** para el desarrollo rápido de aplicaciones web.
- **Monitorización Exhaustiva y Multifacética:**
    - Monitorización de Deriva de Datos/Concepto y Rendimiento: **Evidently AI**.
    - Métricas de Salud Operacional (latencia, errores, uso de recursos): **Prometheus y Grafana**.
    - Sistema de Alertas: **Prometheus Alertmanager** integrado con herramientas de monitorización.
- **Pipeline Detallado de CI/CD/CT (Integración Continua/Entrega Continua/Entrenamiento Continuo):**
    - **Disparadores (Triggers):** Commits a la rama principal en GitHub, nuevas etiquetas de versión de datos en DVC, alertas de monitorización.
    - **CI (GitHub Actions):** Clonación de código, obtención de datos de DVC, pruebas unitarias/de integración.
    - **CT (MLflow):** Ejecución de scripts de entrenamiento, registro de parámetros, métricas, artefactos.
    - **Validación dentro de CI/CD:** Evaluación automatizada contra el "Sistema de Puntuación de Pruebas de ML", generación de informes XAI.
    - **CD (GitHub Actions, Argo Rollouts):** Actualización del Registro de Modelos de MLflow, construcción de imagen Docker (vía GitHub Packages), despliegue seguro a Kubernetes (EKS) usando estrategias como **Canary o Blue/Green vía Argo Rollouts**.
- **Marco de Gobernanza del Modelo:**
    - Requisitos para **Documentación Exhaustiva** (modelo, datos, procesos, validación, decisiones de diseño).
    - **Auditorías Periódicas** para cumplimiento, ética y rendimiento.
    - **Planes de Mitigación de Riesgos** para posibles fallos del modelo, sesgos o problemas de seguridad.
    - **Gestión del Ciclo de Vida del Modelo** con políticas para el retiro/archivo de modelos.

### Modificado

#### General
- **Alcance y Especificidad del Pipeline:** Se pasó de un esquema general de predicción de enfermedades a un pipeline altamente detallado y especializado para el apoyo diagnóstico de EHs, enfatizando MLOps.
- **Herramientas y Tecnología:** Conceptos vagos reemplazados por tecnologías específicas, justificadas, de código abierto y en la nube en casi todas las etapas.
- **Justificación:** Cada elección significativa de herramienta o metodología ahora va acompañada de una razón fundamental.

#### Fase 1: Diseño
- **Objetivo:** El objetivo general de identificar enfermedades raras se acotó y expandió para incluir la reducción del tiempo de diagnóstico de EHs y enfatizar su rol como herramienta de apoyo.
- **KPIs:** De dos KPIs generales a un conjunto estructurado de indicadores primarios y secundarios, con métricas específicas como Recall y VPP para EHs siendo críticas.
- **Datos de Entrada:** De una lista básica de síntomas + demografía a un enfoque estructurado usando ontologías médicas (SNOMED CT), herramientas de NLP (MedCAT) y un historial clínico/familiar más detallado.
- **Datos de Salida:** De cuatro estados generales de enfermedad a una salida multifacética que incluye niveles de sospecha de EH, EHs candidatas específicas, puntuaciones de confianza, indicadores de urgencia y explicaciones XAI.
- **Limitaciones y Restricciones:** Preocupaciones generales expandidas con estrategias de mitigación específicas y un análisis más profundo de las regulaciones de privacidad y el manejo de sesgos.

#### Fase 2: Desarrollo
- **Fuentes de datos:** Fuentes genéricas ("registros médicos", "bases de datos") reemplazadas por estándares específicos (FHIR), bases de datos nombradas (Orphanet, OMIM) y técnicas (NLP con BioBERT/SciBERT).
- **Manejo de los datos:** Pasos de alto nivel (limpieza, transformación, versionamiento, balanceo) ahora tienen herramientas y técnicas específicas de vanguardia asignadas (Pandas, Dask, ARX, DVC, SMOTE, Feast, Airflow).
- **Modelos de ML a usar:** Una lista amplia de modelos potenciales (RF, GB, SVM, NNs, TL) se acotó a un conjunto inicial bien justificado para comparación (XGBoost, RF, MLP) con seguimiento de experimentos integrado (MLflow) y XAI (SHAP).
- **Validación y Testeo:** Conceptos generales (CV estratificada, métricas) significativamente expandidos con estrategias específicas (conjunto de prueba hold-out, Sistema formal de Puntuación de Pruebas) y herramientas dedicadas para pruebas de sesgo y robustez.

#### Fase 3: Producción
- **Despliegue:** El concepto básico de Docker + Nube + API REST se expandió masivamente con frameworks de servicio específicos (FastAPI), orquestación (Kubernetes/EKS), registro de modelos (MLflow), herramientas de UI (Streamlit) y estrategias de despliegue avanzadas (Canary/Blue-Green con Argo Rollouts).
- **Monitorización:** Conceptos generales de monitorización (métricas, deriva) concretados con herramientas específicas (Evidently AI, Prometheus, Grafana) para distintos aspectos de la monitorización (rendimiento, deriva, salud operacional, alertas).
- **Reentrenamiento:** El reentrenamiento periódico/disparado conceptual evolucionó a un pipeline CI/CD/CT completamente detallado con disparadores, pasos y tecnologías definidos.

### Eliminado
- **Visión Excesivamente Simplista:** La naturaleza de alto nivel y menos detallada del pipeline antiguo.
- **Vaguedad en las Herramientas:** La falta de menciones específicas de herramientas en el pipeline antiguo.
- **Support Vector Machines (SVMs)** y **"Redes neuronales tradicionales"** como opciones iniciales explícitamente nombradas en la sección "Modelos de ML a usar" (aunque podrían explorarse más tarde, el nuevo pipeline especifica un conjunto inicial más enfocado: XGBoost, RF, MLP).

## [0.1.0] - (Esquema Inicial del Pipeline Antiguo)

Esta versión describía un pipeline de ML general y de alto nivel para predecir si un paciente podría sufrir *alguna* enfermedad basándose en síntomas. Sirvió como un esquema conceptual inicial.

- **Fase de Diseño:**
    - Objetivo: Ayuda general para la identificación temprana de enfermedades (especialmente huérfanas).
    - KPIs: Reducción del tiempo promedio de diagnóstico, aumento de la tasa de pacientes derivados correctamente.
    - Datos de Entrada: Lista de síntomas del paciente, datos demográficos básicos (edad, género, peso).
    - Datos de Salida: Clasificación en cuatro estados: no enfermo, enfermedad leve, enfermedad aguda, enfermedad crónica.
    - Limitaciones: Subjetividad de los síntomas, inconsistencia de datos, privacidad del paciente, consecuencias éticas de un diagnóstico erróneo.
- **Fase de Desarrollo:**
    - Fuentes de Datos: Registros médicos, bases de datos existentes sobre enfermedades, estudios sobre enfermedades huérfanas.
    - Manejo de Datos: Mención de alto nivel de ingesta automatizada, limpieza de datos, transformación, estructuración de datos de síntomas, anonimización, versionamiento de datos, ingeniería de características, balanceo de datos.
    - Modelos de ML: Sugeridos Random Forest, Gradient Boosting, Support Vector Machines, Redes Neuronales tradicionales, Transfer Learning.
    - Validación: Mención de validación cruzada estratificada, métricas clave (Recall, Precision, F1-score, AUC-PR), pruebas de sesgo y análisis de errores.
- **Fase de Producción:**
    - Despliegue: Visualizado como un contenedor Docker, desplegado en la nube (AWS, Azure, Google Cloud), accesible mediante una API REST.
    - Monitorización: Monitorización constante del rendimiento del modelo usando métricas clave, generación de alertas por fallos, monitorización de deriva de datos/concepto.
    - Reentrenamiento: Reentrenamiento periódico del modelo con nuevos datos, potencialmente disparado por la degradación del rendimiento.
- **Incluido:** Un diagrama de flujo de alto nivel del pipeline.