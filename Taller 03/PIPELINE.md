# Pipeline de Machine Learning para la Detección Temprana de Enfermedades Huérfanas

## Contexto y Motivación

Las enfermedades huérfanas (EHs), también conocidas como enfermedades raras, afectan a un número reducido de personas en comparación con la población general, pero colectivamente representan un desafío significativo para la salud pública. Uno de los mayores obstáculos es el diagnóstico tardío, que puede llevar años, sometiendo a los pacientes y sus familias a una "odisea diagnóstica" con considerable sufrimiento y empeoramiento de los pronósticos. El objetivo de este pipeline es definir el proceso completo para desarrollar, desplegar y mantener un sistema de Machine Learning (ML) que sirva como herramienta de apoyo a los profesionales de la salud. Este sistema analizará los síntomas y datos del paciente para predecir la posible presencia de una EH, buscando así acortar los tiempos de diagnóstico, facilitar derivaciones más certeras y, en última instancia, mejorar la calidad de vida de los pacientes afectados.

El desafío consiste en definir un pipeline de ML en donde se describa, de manera general, el proceso completo end-to-end para el desarrollo de un modelo capaz de predecir, dados los síntomas de un paciente, si es posible o no que sufra de alguna enfermedad, con un enfoque especial en la detección temprana de enfermedades huérfanas (EHs).

A continuación, se divide el proceso de construcción del pipeline en tres etapas: diseño, desarrollo y producción.

---

## Fase 1: Diseño y Planificación (Estratégica)

1.  **Objetivo:**
    *   Ayudar a los profesionales de la salud a identificar tempranamente enfermedades, con un enfoque especial en las enfermedades huérfanas (EHs).
    *   Reducir el tiempo de diagnóstico de EHs.
    *   Servir como una herramienta de apoyo a la decisión clínica, no como sustituto del juicio médico.

2.  **KPIs (Indicadores Clave de Rendimiento):**
    *   **Primarios:**
        *   Reducción del tiempo promedio de diagnóstico para EHs identificadas.
        *   Aumento de la tasa de derivación correcta (pacientes con sospecha de EH que resultan positivos tras estudios confirmatorios).
        *   Sensibilidad (Recall) para EHs: Maximizar la detección de EHs reales.
        *   Valor Predictivo Positivo (VPP) para EHs.
    *   **Secundarios:**
        *   Tasa de adopción por profesionales de la salud.
        *   Satisfacción del usuario (médicos).

3.  **Datos de Entrada:**
    *   **Listado de síntomas del paciente:**
        *   Se utilizará **SNOMED CT (Systematized Nomenclature of Medicine - Clinical Terms)** como ontología médica para la estandarización.
            *   *Justificación:* SNOMED CT es una terminología clínica multilingüe y completa, reconocida globalmente, que cubre una amplia gama de conceptos clínicos, incluyendo síntomas, hallazgos, enfermedades, procedimientos, etc. Su estructura jerárquica permite diferentes niveles de granularidad y facilita la interoperabilidad.
        *   *Guía para la entrada de datos y estandarización ontológica:* Se proporcionará a los usuarios una interfaz con campos estructurados para los síntomas principales, y un campo de texto libre para síntomas adicionales o matices. Se recomendará el uso de terminología lo más precisa posible (ej. "fiebre intermitente superior a 38.5°C" en lugar de solo "fiebre"). Para el texto libre, se implementará un mapeo asistido:
            *   Si los síntomas se ingresan como texto libre, se utilizará **MedCAT (Medical Concept Annotation Tool)** para mapearlos a códigos SNOMED CT.
                *   *Justificación:* MedCAT es una herramienta open-source especializada en la extracción de conceptos médicos de texto no estructurado y su vinculación a ontologías como SNOMED CT. Es personalizable y ha demostrado buen rendimiento en tareas de NER (Named Entity Recognition) y vinculación en el dominio biomédico.
    *   **Datos demográficos básicos:** Edad (en años y meses para pediátricos), género asignado al nacer.
    *   **Datos clínicos adicionales (si disponibles):** Peso (kg), altura (cm), historial familiar relevante (especialmente presencia de EHs o síntomas inexplicables en familiares de primer grado).

4.  **Ejemplo de Datos de Entrada y Salida:**
    *   **Ejemplo de Datos de Entrada (simplificado):**
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
    *   **Ejemplo de Datos de Salida (simplificado):**
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

5.  **Limitaciones y Restricciones Ético-Legales:**
    *   Subjetividad y variabilidad de síntomas: Los síntomas pueden ser reportados o interpretados de forma diferente. Mitigar con guías claras para la entrada de datos y estandarización ontológica.
    *   Privacidad y Seguridad de los Datos: Cumplimiento estricto de regulaciones como GDPR (Europa), HIPAA (EE. UU.) o leyes locales de protección de datos personales y de salud.
        *   *Estrategia:* Anonimización/pseudonimización robusta, cifrado de datos en reposo y en tránsito, control de acceso basado en roles (RBAC), auditorías de acceso. Considerar Data Clean Rooms si se comparten datos agregados con terceros.
    *   Consecuencias Éticas:
        *   El modelo debe ser una herramienta de apoyo, y la decisión final siempre recae en el profesional clínico.
        *   Manejo cuidadoso de falsos positivos (pueden generar ansiedad innecesaria y costes de pruebas adicionales) y, críticamente, falsos negativos (pueden retrasar un diagnóstico vital, especialmente en EHs).
    *   Sesgos en los datos: Las EHs son, por definición, raras, lo que lleva a datos inherentemente desbalanceados. Los datos históricos pueden reflejar sesgos socioeconómicos, geográficos o de acceso previo al sistema de salud, que el modelo podría aprender y perpetuar.

---

## Fase 2: Desarrollo (Táctica y Operativa)

1.  **Adquisición y Fuentes de Datos:**
    *   **Registros Médicos Electrónicos (EHRs/HCEs):**
        *   Se utilizará el estándar **HL7 FHIR (Fast Healthcare Interoperability Resources)** para la integración.
            *   *Justificación:* FHIR es un estándar moderno diseñado para el intercambio electrónico de información sanitaria. Utiliza tecnologías web actuales (RESTful APIs, JSON/XML), lo que facilita la integración con sistemas modernos y el acceso a recursos de datos granulares (como Observation para síntomas, Patient para demográficos, FamilyMemberHistory). Esto permite una extracción de datos más eficiente y estandarizada en comparación con procesos ETL tradicionales que pueden ser específicos de cada sistema EHR.
    *   **Bases de Datos Especializadas en Enfermedades Huérfanas:**
        *   **Orphanet** (para datos de prevalencia, genes, síntomas asociados a EHs vía HPO, que se mapearán a SNOMED CT cuando sea necesario), **OMIM**.
    *   **Literatura Científica y Estudios Clínicos:**
        *   La tecnología NLP, como modelos **BioBERT** o **SciBERT** (pre-entrenados en literatura biomédica), se usará para extraer relaciones síntoma-enfermedad. Esto funciona identificando entidades (síntomas, enfermedades) en el texto y luego clasificando la relación entre ellas (ej. "causa", "asociado con", "manifiesta como") basándose en el contexto lingüístico aprendido durante el entrenamiento del modelo en grandes corpus de textos médicos.
    *   **Almacenamiento de Datos Crudos (Data Lake):**
        *   *Tecnología:* **AWS S3**.
            *   *Justificación:* Ofrece escalabilidad masiva, alta durabilidad, es costo-efectivo para grandes volúmenes de datos, y se integra nativamente con una amplia gama de servicios de AWS que podrían usarse en el pipeline.

2.  **Preprocesamiento y Manejo de los Datos (Data Pipeline):**
    *   **Orquestación del Pipeline de Datos:**
        *   Se utilizará **Apache Airflow**.
            *   *Justificación:* Airflow es una plataforma robusta y ampliamente adoptada para la orquestación de flujos de trabajo, escrita en Python, lo que facilita su uso por equipos de ciencia de datos. Permite definir DAGs complejos, programar tareas, gestionar dependencias y monitorizar ejecuciones.
    *   **Ingesta Automatizada:** Scripts Python utilizando las APIs FHIR y conectores a las bases de datos.
    *   **Limpieza de Datos:** Pandas, Dask (para datasets grandes).
    *   **Transformación y Estandarización:** Mapeo a SNOMED CT (con MedCAT si es texto libre), codificación de variables categóricas, escalado de variables numéricas (usando Scikit-learn).
    *   **Estructuración de Datos de Síntomas (Feature Engineering):** Creación de perfiles de síntomas (vectores SNOMED CT), embeddings.
    *   **Anonimización/Pseudonimización Robusta:** Utilizando **ARX De-Identification Tool**.
    *   **Versionamiento de Datos:**
        *   Se utilizará **DVC (Data Version Control)**.
            *   *Justificación:* DVC permite versionar grandes archivos de datos y modelos de ML de la misma manera que Git versiona el código, pero sin almacenar los archivos grandes directamente en el repositorio. En su lugar, DVC almacena metarchivos pequeños que apuntan a los datos reales.
    *   **Balanceo de Datos:**
        *   Se utilizará **SMOTE (Synthetic Minority Over-sampling Technique)** de la librería `imbalanced-learn`.
            *   *Justificación:* SMOTE es una técnica popular y efectiva para generar muestras sintéticas de la clase minoritaria (EHs), ayudando a balancear el dataset y mejorar el rendimiento del modelo en la detección de estas enfermedades raras.
    *   **Almacenamiento de Datos Procesados y Características (Feature Store):**
        *   Se utilizará **Feast**.
            *   *Justificación:* Feast es un feature store open-source que permite definir, gestionar, servir y descubrir características de ML. Se integra con almacenamiento offline y online. Esto asegura consistencia entre entrenamiento y servicio.

3.  **Desarrollo y Entrenamiento de Modelos de ML:**
    *   **Selección de Modelos:** Se entrenarán y evaluarán inicialmente tres tipos de modelos para comparar su rendimiento en esta tarea específica:
        *   **XGBoost (Extreme Gradient Boosting):** Es un algoritmo de boosting de gradiente altamente eficiente y efectivo, que a menudo proporciona un rendimiento de vanguardia en datos tabulares. Es robusto a outliers, maneja bien valores faltantes y ofrece cierta interpretabilidad (importancia de características).
        *   **Random Forest:** Es un modelo de ensamblaje que promedia múltiples árboles de decisión, lo que lo hace robusto al sobreajuste y fácil de usar. También proporciona métricas de importancia de características.
        *   **Red Neuronal Multicapa (MLP) simple con TensorFlow/Keras:** Para explorar si las representaciones no lineales aprendidas por una red neuronal pueden capturar patrones complejos en los datos de síntomas que los modelos de árboles podrían pasar por alto, especialmente si se utilizan embeddings de síntomas. Se monitoreará el rendimiento de estos tres modelos en la plataforma de experimentación para decidir cuál es el más apropiado o si una combinación (ensemble) es superior.
    *   **Plataforma de Experimentación y Seguimiento de ML:**
        *   Se utilizará **MLflow Tracking**.
            *   *Justificación:* MLflow es una plataforma open-source para gestionar el ciclo de vida del ML, incluyendo el seguimiento de experimentos (parámetros, código, datos, métricas), empaquetado de modelos y gestión de modelos. Es agnóstico a la nube y a las librerías de ML.
    *   **Explainable AI (XAI):**
        *   Se utilizará **SHAP (SHapley Additive exPlanations)**.
            *   *Justificación:* SHAP proporciona explicaciones consistentes y localmente precisas para las predicciones de cualquier modelo, ayudando a entender qué características influyen más en una predicción específica.

4.  **Validación y Testeo Riguroso:**
    *   **Estrategia de Validación:**
        *   **Validación Cruzada Estratificada (Stratified K-Fold Cross-Validation):** Para asegurar que la proporción de clases (especialmente las EHs minoritarias) se mantenga en cada fold de entrenamiento/validación.
        *   **Conjunto de Prueba (Hold-out Test Set):** Un conjunto de datos completamente separado, no utilizado durante el desarrollo o ajuste de hiperparámetros, para obtener una estimación insesgada del rendimiento del modelo final.
    *   **Métricas Clave (especialmente para clases minoritarias como EHs):**
        *   Recall por clase, especialmente para cada EH o categoría de EH.
        *   Precisión por clase.
        *   F1-Score (macro, micro, ponderado, y por clase).
        *   Área Bajo la Curva de Precisión-Recall (AUC-PR), especialmente importante para datos desbalanceados, ya que se enfoca mejor en el rendimiento de la clase positiva minoritaria.
        *   Matriz de confusión detallada, analizando errores específicos.
    *   **Sistema de Puntuación de Pruebas de ML (ML Test Score System) / Framework de Evaluación de Modelos:**
        *   Con el fin de evaluar cuál modelo será desplegado en producción. Esto incluye no solo métricas de rendimiento globales, sino también el rendimiento en segmentos críticos de datos (ej. EHs específicas, diferentes grupos demográficos) y los resultados de las pruebas de sesgo.
            *   *Justificación:* Asegura una evaluación consistente, objetiva y comparable de los modelos a lo largo del tiempo y entre diferentes versiones.
    *   **Pruebas de Sesgo (Bias Testing):**
        *   Evaluar el rendimiento del modelo (Sensibilidad, Precisión, tasas de error) en diferentes subgrupos demográficos (edad, género, etnia si está disponible y es éticamente permisible y relevante) para asegurar equidad y detectar posibles sesgos perjudiciales.
        *   *Tecnología:* Aequitas, IBM AI Fairness 360, Fairlearn.
    *   **Análisis de Errores:**
        *   Revisión manual y cualitativa de falsos positivos y falsos negativos (especialmente para EHs) por expertos clínicos para identificar patrones, debilidades del modelo y áreas de mejora.
    *   **Pruebas de Robustez:** Evaluar cómo se comporta el modelo ante pequeñas perturbaciones en los datos de entrada o ante datos ligeramente fuera de la distribución de entrenamiento.

---

## Fase 3: Producción y Operacionalización (MLOps)

1.  **Despliegue del Modelo:**
    *   **Empaquetado del Modelo:** Docker.
    *   **Servicio del Modelo (Model Serving):**
        *   El modelo se expondrá como un servicio a través de una **API REST** utilizando **FastAPI**, desplegado en **Kubernetes (Amazon EKS - Elastic Kubernetes Service)**.
            *   *Justificación:* FastAPI es un framework web Python moderno, de alto rendimiento, fácil de usar y que genera automáticamente documentación interactiva (Swagger UI). Kubernetes proporciona una plataforma robusta para orquestar contenedores Docker, ofreciendo escalabilidad automática, auto-reparación, y gestión eficiente de despliegues (ej. rolling updates). Amazon EKS simplifica la ejecución de Kubernetes en AWS.
        *   **Arquitectura Modular y Débilmente Acoplada:** El servicio del modelo será un componente independiente. Otras partes del sistema (como la ingesta de datos, preprocesamiento, monitorización o la interfaz de usuario) también pueden ser servicios separados, comunicándose a través de APIs.
    *   **Registro del Modelo:** MLflow Model Registry.
    *   **Interfaz de Usuario (Front-End):**
        *   Se desarrollará una aplicación web inicial utilizando **Streamlit**.
            *   *Justificación:* Streamlit permite crear rápidamente aplicaciones web interactivas y visualizaciones de datos directamente en Python.

2.  **Monitorización Continua y Gestión del Decaimiento del Modelo:**
    *   **Monitorización del Rendimiento, Deriva de Datos/Concepto, Integridad, Sesgos:**
        *   Se utilizará **Evidently AI** para el análisis de deriva de datos, deriva de concepto y rendimiento del modelo.
            *   *Justificación:* Evidently AI es una herramienta open-source que genera informes interactivos y perfiles JSON para monitorizar modelos de ML en producción, enfocándose en la detección de drift y caídas de calidad.
    *   **Monitorización Operacional (Health Operation Metrics):**
        *   Se utilizará **Prometheus** y **Grafana**.
            *   *Justificación:* Prometheus es un sistema de monitorización y alerta open-source líder, y Grafana permite crear dashboards visuales para estas métricas operacionales (latencia, errores, uso de recursos).
    *   **Triggers y Alertas:** Configurados en Prometheus (Alertmanager) y scripts que consuman los reportes de Evidently AI.

3.  **Reentrenamiento y Mantenimiento del Modelo:**
    *   **Estrategia de Reentrenamiento:**
        *   Se optará por una estrategia híbrida de **reentrenamiento periódico en Batch mensual, o cuando un disparador lo indique**.
        *   *Justificación:* Para un sistema crítico de salud, la estabilidad y la validación exhaustiva de cada nueva versión del modelo son primordiales. El reentrenamiento en batch permite un control completo sobre el proceso de validación antes de que un nuevo modelo entre en producción, minimizando riesgos.

4.  **Flujo Detallado del Pipeline CI/CD/CT y Tecnologías:**
    *   **Disparador (Trigger):** Un commit a la rama principal en **GitHub** del código del modelo/preprocesamiento, o un nuevo tag de versión de datos en **DVC**, o una alerta de monitorización (**Prometheus/Evidently**).
    *   **CI - Orquestación (Continuous Integration):** **GitHub Actions** detecta el disparador.
        *   Se clona el repositorio Git y obtiene la versión de datos correspondiente usando DVC.
        *   Se ejecutan pruebas unitarias y de integración del código.
    *   **CT - Entrenamiento (Continuous Training):**
        *   Se invoca un script Python que utiliza **MLflow** para iniciar una ejecución de entrenamiento.
        *   El script entrena los tres modelos candidatos (XGBoost, MLP, Random Forest) con los últimos datos aprobados.
        *   Las métricas, parámetros, y artefactos del modelo (modelos serializados) se registran en el servidor de **MLflow Tracking**.
    *   **Validación del Modelo:**
        *   Otro script evalúa los modelos entrenados contra el "ML Test Score System" predefinido (comparando métricas como Sensibilidad para EHs, AUC-PR, etc., con umbrales establecidos).
        *   Se generan reportes de XAI (SHAP) para el mejor modelo.
    *   **CD - Entrega/Despliegue (Continuous Delivery/Deployment):**
        *   Si un modelo supera todas las pruebas de validación y es aprobado (manual o automáticamente):
            *   El modelo se registra en el **MLflow Model Registry**, promoviéndolo a "staging" o "production".
            *   **GitHub Actions** construye una nueva imagen **Docker** para el servicio de inferencia (FastAPI) con el modelo actualizado.
            *   La imagen Docker se sube a un registro de contenedores (**GitHub Packages**).
            *   Se realiza un despliegue en el clúster de **Kubernetes (EKS)** utilizando una estrategia de despliegue seguro como Canary o Blue/Green, gestionada por herramientas como **Argo Rollouts** (integrado con Kubernetes). Esto permite una liberación gradual y la posibilidad de rollback rápido si se detectan problemas en producción.
        *   El sistema de monitorización (**Prometheus/Evidently/Grafana**) observa el modelo en producción y puede volver a disparar el pipeline si es necesario.

5.  **Gobernanza del Modelo:**
    *   **Documentación Exhaustiva:** Mantener documentación detallada del modelo, sus versiones, los datos de entrenamiento, los procesos de preprocesamiento, los resultados de validación, las decisiones de diseño, y el rendimiento en producción.
    *   **Auditorías Periódicas:** Realizar auditorías del modelo y del pipeline para asegurar el cumplimiento normativo, ético y de rendimiento.
    *   **Plan de Mitigación de Riesgos:** Tener planes para abordar posibles fallos del modelo, sesgos detectados, o problemas de seguridad.
    *   **Gestión del Ciclo de Vida del Modelo:** Definir políticas para cuándo un modelo debe ser retirado o archivado.

---