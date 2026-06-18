# Desafío 4 — Motor de Clasificación de Datos con IA

Motor que usa un **LLM compatible con OpenAI** (por defecto **OpenRouter**) para
clasificar textos cortos por **sensibilidad**, **categoría** y **riesgo** —
pensado para un equipo de ciberseguridad / data security.

## Diseño

Cada responsabilidad vive en su propio módulo, y el motor depende de una
*interfaz* del cliente LLM (no del SDK concreto). Esto mantiene el código
legible, testeable y desacoplado del proveedor:

| Módulo | Responsabilidad |
|--------|-----------------|
| `models.py` | Taxonomía (enums) y `ClassificationResult`. Única fuente de verdad de las etiquetas. |
| `config.py` | Configuración (API key, base_url, modelo). Carga desde variables de entorno. |
| `prompts.py` | Construcción del prompt a partir de la taxonomía. |
| `llm_client.py` | Interfaz `LLMClient` + implementación OpenAI-compatible. |
| `engine.py` | Orquesta: prompt → LLM → parseo → validación → resultado tipado. |
| `retry.py` | Reintentos con backoff exponencial (genérico y testeable). |
| `redaction.py` | Enmascara datos sensibles antes de loguear. |
| `cli.py` | Demo en vivo por línea de comandos. |
| `tests/` | Tests con un cliente LLM falso (sin red). |

**Principios aplicados:** responsabilidad única por módulo, inversión de
dependencias (el motor depende del `Protocol` `LLMClient`), y una sola fuente de
verdad para la taxonomía (el prompt y la validación se derivan de los mismos enums).

## Taxonomía

- **Sensibilidad:** `PUBLIC`, `INTERNAL`, `CONFIDENTIAL`, `RESTRICTED`
- **Categoría:** `PII`, `PCI`, `PHI`, `CREDENTIALS`, `FINANCIAL`, `INTELLECTUAL_PROPERTY`, `GENERAL`
- **Riesgo:** `LOW`, `MEDIUM`, `HIGH`, `CRITICAL`

## Features adicionales

- **Confianza (`confidence`)**: cada clasificación incluye un score 0.0–1.0 (se
  valida y se recorta al rango).
- **Reintentos con backoff**: ante timeouts, rate limits o errores 5xx el cliente
  reintenta automáticamente (configurable con `LLM_MAX_ATTEMPTS`).
- **Soporte `.env`**: si existe un `.env` y `python-dotenv` está instalado, se
  cargan las variables automáticamente (la API key nunca se commitea).
- **Logging con redacción**: con `-v` se ven logs de progreso, pero los datos
  sensibles (tarjetas, DNI, emails, tokens) se enmascaran antes de loguearse.
- **`muestras.txt`**: set de ejemplos listo para la demo.

## Uso (demo en vivo)

1. Instalar dependencias:

   ```bash
   pip install -r ../requirements.txt
   ```

2. Configurar la API key (OpenRouter o compatible), por env var o `.env`:

   ```bash
   export LLM_API_KEY="sk-or-..."
   # Opcionales:
   export LLM_BASE_URL="https://openrouter.ai/api/v1"
   export LLM_MODEL="openai/gpt-4o-mini"
   export LLM_MAX_ATTEMPTS="3"
   ```

3. Ejecutar:

   ```bash
   # Un texto
   python -m challenge_4_classification_engine.cli "Mi tarjeta es 4111 1111 1111 1111"

   # Con logs (datos sensibles redactados)
   python -m challenge_4_classification_engine.cli -v "DNI 30.123.456"

   # Varias muestras desde el archivo de ejemplo (una por línea)
   cat challenge_4_classification_engine/muestras.txt | \
     python -m challenge_4_classification_engine.cli
   ```

Salida (JSON):

```json
[
  {
    "text": "Mi tarjeta es 4111 1111 1111 1111",
    "sensitivity": "RESTRICTED",
    "category": "PCI",
    "risk": "CRITICAL",
    "rationale": "Contiene un número de tarjeta de crédito.",
    "confidence": 0.97
  }
]
```

## Tests

```bash
pytest challenge_4_classification_engine
```

Los tests usan un cliente falso, por lo que **no requieren API key ni red**.
