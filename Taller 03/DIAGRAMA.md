```mermaid
graph TD
    %% Disparadores (Triggers)
    T1["GitHub Commit<br/>(Modelo/Preproc)"]
    T2["DVC Tag<br/>(Nuevos Datos)"]
    T3["Alerta Monitor.<br/>(Prometheus/Evid.)"]

    %% Fuentes de Datos
    subgraph "Fuentes de Datos"
        DS1["EHRs<br/>(HL7 FHIR)"]
        DS2["Orphanet<br/>(EHs Database)"]
        DS3["Literatura Científica<br/>(BioBERT/SciBERT)"]
    end

    subgraph "Ingesta y Procesamiento"
        ING1["Orquestación<br/>(Apache Airflow)"]
        ING2["Extracción APIs<br/>(FHIR, Orphanet)"]
        ING3["Almacén Datos Crudos<br/>(AWS S3 Data Lake)"]
        ING4["Limpieza y Transform.<br/>(Pandas/Dask)"]
        ING5["Mapeo SNOMED CT<br/>(MedCAT)"]
        ING6["Anonimización<br/>(ARX Tool)"]
        ING7["Balanceo Datos<br/>(SMOTE)"]
        ING8["Feature Store<br/>(Feast)"]
        ING9["Versionado Datos<br/>(DVC)"]
    end

    subgraph "CI (GitHub Actions)"
        CI1["Clonar Repo Git"]
        CI2["Obtener Datos DVC"]
        CI3["Pruebas Código<br/>(Unit/Integr.)"]
    end

    subgraph "CT (GitHub Actions)"
        CT1["MLflow Script<br/>(Python)"]
        CT2["Entrenar Modelos<br/>(XGB, MLP, RF)<br/>(Datos DVC/Feast)"]
        CT3["Registrar Experim.<br/>(MLflow Tracking)"]
    end

    subgraph "Validación (GitHub Actions)"
        VAL1["Evaluar Modelos<br/>(ML Test Score)"]
        VAL2["Comparar Métricas<br/>(Sensib., AUC-PR)"]
        VAL3["Reportes XAI (SHAP)<br/>(Mejor Modelo)"]
        VAL4{"Aprobado?"}
    end

    subgraph "CD (GitHub Actions)"
        CD1["Registrar Modelo<br/>(MLflow Registry)"]
        CD2["Build Imagen Docker<br/>(FastAPI+Modelo)"]
        CD3["Push Docker<br/>(GitHub Packages)"]
        CD4["Deploy K8s (EKS)<br/>(Argo Rollouts)"]
    end

    subgraph "Monitorización Prod."
        MON_NODE["Modelo en Prod.<br/>(FastAPI en EKS)"]
        MON_TOOLS["Monitorización<br/>(Prometh/Graf/Evid)"]
    end

    %% Flujo de Ingesta de Datos
    DS1 --> ING1;
    DS2 --> ING1;
    DS3 --> ING1;
    
    ING1 --> ING2;
    ING2 --> ING3;
    ING3 --> ING4;
    ING4 --> ING5;
    ING5 --> ING6;
    ING6 --> ING7;
    ING7 --> ING8;
    ING8 --> ING9;
    
    %% Conexión con el pipeline principal
    ING9 --> T2;

    %% Flujo del Pipeline Principal
    T1 --> CI1;
    T2 --> CI1;
    T3 --> CI1;

    CI1 --> CI2;
    CI2 --> CI3;
    CI3 --> CT1;

    CT1 --> CT2;
    CT2 --> CT3;
    CT3 --> VAL1;

    VAL1 --> VAL2;
    VAL2 --> VAL3;
    VAL3 --> VAL4;

    VAL4 -- "Sí" --> CD1;
    VAL4 -- "No (Rev.)" --> CT1;

    CD1 --> CD2;
    CD2 --> CD3;
    CD3 --> CD4;
    CD4 --> MON_NODE;

    MON_TOOLS --> T3;
    MON_NODE --> MON_TOOLS;

    %% Estilos
    classDef trigger fill:#d63384,stroke:#333,stroke-width:2px,color:#fff;
    classDef data_sources fill:#17a2b8,stroke:#333,stroke-width:2px,color:#fff;
    classDef ingestion fill:#28a745,stroke:#333,stroke-width:2px,color:#fff;
    classDef ci fill:#0d6efd,stroke:#333,stroke-width:2px,color:#fff;
    classDef ct fill:#198754,stroke:#333,stroke-width:2px,color:#fff;
    classDef class_val fill:#fd7e14,stroke:#333,stroke-width:2px,color:#fff;
    classDef cd fill:#dc3545,stroke:#333,stroke-width:2px,color:#fff;
    classDef mon_style fill:#6f42c1,stroke:#333,stroke-width:2px,color:#fff;

    class T1,T2,T3 trigger;
    class DS1,DS2,DS3 data_sources;
    class ING1,ING2,ING3,ING4,ING5,ING6,ING7,ING8,ING9 ingestion;
    class CI1,CI2,CI3 ci;
    class CT1,CT2,CT3 ct;
    class VAL1,VAL2,VAL3,VAL4 class_val;
    class CD1,CD2,CD3,CD4 cd;
    class MON_NODE,MON_TOOLS mon_style;