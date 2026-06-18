"""
Tests del motor de clasificación (Desafío 4).

Se usa un cliente LLM falso que devuelve respuestas controladas, de modo que
los tests no dependen de la red ni de una API key.
"""

import os
import sys

import pytest

# Permite importar el paquete desde la raíz del repo.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from challenge_4_classification_engine.engine import (  # noqa: E402
    ClassificationError,
    DataClassifier,
)
from challenge_4_classification_engine.models import (  # noqa: E402
    Category,
    RiskLevel,
    SensitivityLevel,
)


class FakeClient:
    """Cliente LLM falso: devuelve siempre la respuesta predefinida."""

    def __init__(self, response: str) -> None:
        self._response = response

    def complete(self, system_prompt: str, user_prompt: str) -> str:
        return self._response


def test_clasificacion_valida():
    response = (
        '{"sensitivity": "RESTRICTED", "category": "PCI", '
        '"risk": "CRITICAL", "rationale": "Contiene un número de tarjeta."}'
    )
    classifier = DataClassifier(FakeClient(response))
    result = classifier.classify("Mi tarjeta es 4111 1111 1111 1111")

    assert result.sensitivity is SensitivityLevel.RESTRICTED
    assert result.category is Category.PCI
    assert result.risk is RiskLevel.CRITICAL
    assert "tarjeta" in result.rationale.lower()


def test_json_envuelto_en_markdown():
    response = (
        "```json\n"
        '{"sensitivity": "PUBLIC", "category": "GENERAL", '
        '"risk": "LOW", "rationale": "Texto informativo."}\n'
        "```"
    )
    classifier = DataClassifier(FakeClient(response))
    result = classifier.classify("El clima de hoy es soleado")
    assert result.sensitivity is SensitivityLevel.PUBLIC
    assert result.category is Category.GENERAL


def test_etiqueta_invalida_lanza_error():
    response = (
        '{"sensitivity": "TOP_SECRET", "category": "PII", '
        '"risk": "HIGH", "rationale": "x"}'
    )
    classifier = DataClassifier(FakeClient(response))
    with pytest.raises(ClassificationError):
        classifier.classify("texto cualquiera")


def test_respuesta_sin_json_lanza_error():
    classifier = DataClassifier(FakeClient("no tengo idea"))
    with pytest.raises(ClassificationError):
        classifier.classify("texto cualquiera")


def test_texto_vacio_lanza_value_error():
    classifier = DataClassifier(FakeClient("{}"))
    with pytest.raises(ValueError):
        classifier.classify("   ")


def test_to_dict_es_serializable():
    response = (
        '{"sensitivity": "INTERNAL", "category": "FINANCIAL", '
        '"risk": "MEDIUM", "rationale": "Datos internos."}'
    )
    classifier = DataClassifier(FakeClient(response))
    data = classifier.classify("Balance Q3").to_dict()
    assert data["sensitivity"] == "INTERNAL"
    assert data["category"] == "FINANCIAL"
    assert data["risk"] == "MEDIUM"


def test_classify_many():
    response = (
        '{"sensitivity": "PUBLIC", "category": "GENERAL", '
        '"risk": "LOW", "rationale": "ok"}'
    )
    classifier = DataClassifier(FakeClient(response))
    results = classifier.classify_many(["uno", "dos", "tres"])
    assert len(results) == 3
