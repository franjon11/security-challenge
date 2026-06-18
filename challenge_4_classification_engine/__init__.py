"""
Desafío 4 — Motor de clasificación de datos con IA.

Clasifica textos cortos por sensibilidad, categoría y riesgo usando un LLM
compatible con OpenAI (por ejemplo, OpenRouter).

Lenguaje: Python 3.12
"""

from .config import Config
from .engine import DataClassifier
from .models import (
    Category,
    ClassificationResult,
    RiskLevel,
    SensitivityLevel,
)

__all__ = [
    "Config",
    "DataClassifier",
    "Category",
    "ClassificationResult",
    "RiskLevel",
    "SensitivityLevel",
]
