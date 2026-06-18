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
| `cli.py` | Demo en vivo por línea de comandos. |
| `tests/` | Tests con un cliente LLM falso (sin red). |

**Principios aplicados:** responsabilidad única por módulo, inversión de
dependencias (el motor depende del `Protocol` `LLMClient`), y una sola fuente de
verdad para la taxonomía (el prompt y la validación se derivan de los mismos enums).

## Taxonomía

- **Sensibilidad:** `PUBLIC`, `INTERNAL`, `CONFIDENTIAL`, `RESTRICTED`
- **Categoría:** `PII`, `PCI`, `PHI`, `CREDENTIALS`, `FINANCIAL`, `INTELLECTUAL_PROPERTY`, `GENERAL`
- **Riesgo:** `LOW`, `MEDIUM`, `HIGH`, `CRITICAL`

## Uso (demo en vivo)

1. Instalar dependencias:

   ```bash
   pip install -r ../requirements.txt
   ```

2. Configurar la API key (OpenRouter o compatible):

   ```bash
   export LLM_API_KEY="sk-or-..."
   # Opcionales:
   export LLM_BASE_URL="https://openrouter.ai/api/v1"
   export LLM_MODEL="openai/gpt-4o-mini"
   ```

3. Ejecutar:

   ```bash
   # Un texto
   python -m challenge_4_classification_engine.cli "Mi tarjeta es 4111 1111 1111 1111"

   # Varias muestras desde un archivo (una por línea)
   cat muestras.txt | python -m challenge_4_classification_engine.cli
   ```

Salida (JSON):

```json
[
  {
    "text": "Mi tarjeta es 4111 1111 1111 1111",
    "sensitivity": "RESTRICTED",
    "category": "PCI",
    "risk": "CRITICAL",
    "rationale": "Contiene un número de tarjeta de crédito."
  }
]
```

## Tests

```bash
pytest challenge_4_classification_engine
```

Los tests usan un cliente falso, por lo que **no requieren API key ni red**.
