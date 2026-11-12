# ML Platform — Estado del Proyecto

## 1. Objetivo

Construir una plataforma modular en Python para:

- Analizar ventas y datos empresariales.
- Calcular ingresos, costos, utilidad y márgenes.
- Analizar productos, áreas y personal.
- Preparar datos para Power BI.
- Incorporar Machine Learning posteriormente.
- Soportar datos en español e inglés.

## 2. Arquitectura

```text
FUENTES DE DATOS
       ↓
   INGESTION
       ↓
   VALIDACIÓN
       ↓
DETECCIÓN DE COLUMNAS
       ↓
 NORMALIZACIÓN
       ↓
    LIMPIEZA
       ↓
    ANÁLISIS
       ↓
   POWER BI
       ↓
MACHINE LEARNING
```

## 3. Estado actual

- Ingestion implementada.
- CSVReader implementado y probado.
- ExcelReader implementado y probado.
- JSONReader implementado y probado.
- PDFReader implementado y probado.
- TXTReader implementado y probado.
- ReaderFactory implementado y probado.

## 4. Tests

La suite de ingestion contiene 21 tests.

Resultado actual:

```text
21 passed
```

## 5. Próximo paso

Continuar con la siguiente etapa de la arquitectura después de INGESTION.
