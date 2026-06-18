"""
Motor de clasificación.

Orquesta el flujo completo: arma el prompt, llama al LLM, parsea y valida la
respuesta contra la taxonomía y devuelve un `ClassificationResult` tipado.
"""

from __future__ import annotations

import json
import logging

from .llm_client import LLMClient
from .models import (
    Category,
    ClassificationResult,
    RiskLevel,
    SensitivityLevel,
)
from .prompts import SYSTEM_PROMPT, build_user_prompt
from .redaction import redact

logger = logging.getLogger(__name__)


class ClassificationError(Exception):
    """Se lanza cuando la respuesta del LLM no puede parsearse o validarse."""


class DataClassifier:
    """
    Clasifica textos por sensibilidad, categoría y riesgo usando un LLM.

    Depende solo de la interfaz `LLMClient`, por lo que es agnóstico del
    proveedor y fácilmente testeable.
    """

    def __init__(self, client: LLMClient) -> None:
        self._client = client

    def classify(self, text: str) -> ClassificationResult:
        """
        Clasifica un único texto.

        Parameters:
            text (str): texto corto a analizar.

        Returns:
            ClassificationResult: resultado tipado y validado.

        Raises:
            ValueError: si el texto está vacío.
            ClassificationError: si la respuesta del LLM es inválida.
        """
        if not text or not text.strip():
            raise ValueError("El texto a clasificar no puede estar vacío.")

        # Se loguea el texto redactado para no filtrar el dato sensible.
        logger.info("Clasificando texto: %s", redact(text))

        raw_response = self._client.complete(SYSTEM_PROMPT, build_user_prompt(text))
        payload = self._parse_json(raw_response)
        result = self._to_result(text, payload)

        logger.info(
            "Resultado: sensitivity=%s category=%s risk=%s confidence=%s",
            result.sensitivity.value,
            result.category.value,
            result.risk.value,
            result.confidence,
        )
        return result

    def classify_many(self, texts: list[str]) -> list[ClassificationResult]:
        """
        Clasifica una lista de textos, uno por uno.

        Parameters:
            texts (list[str]): textos a analizar.

        Returns:
            list[ClassificationResult]: un resultado por cada texto.
        """
        return [self.classify(text) for text in texts]

    @staticmethod
    def _parse_json(raw_response: str) -> dict:
        """
        Extrae el objeto JSON de la respuesta del modelo.

        Es tolerante a que el modelo envuelva el JSON en texto o en un bloque
        markdown (```json ... ```): se recorta desde la primera '{' hasta la
        última '}'.
        """
        start = raw_response.find("{")
        end = raw_response.rfind("}")
        if start == -1 or end == -1 or end < start:
            raise ClassificationError(
                f"La respuesta del modelo no contiene un objeto JSON: {raw_response!r}"
            )
        try:
            return json.loads(raw_response[start : end + 1])
        except json.JSONDecodeError as exc:
            raise ClassificationError(
                f"No se pudo parsear el JSON de la respuesta: {exc}"
            ) from exc

    @staticmethod
    def _to_result(text: str, payload: dict) -> ClassificationResult:
        """
        Valida el payload contra la taxonomía y construye el resultado.

        Raises:
            ClassificationError: si alguna etiqueta no es válida.
        """
        try:
            return ClassificationResult(
                text=text,
                sensitivity=SensitivityLevel.parse(payload.get("sensitivity", "")),
                category=Category.parse(payload.get("category", "")),
                risk=RiskLevel.parse(payload.get("risk", "")),
                rationale=str(payload.get("rationale", "")).strip(),
                confidence=DataClassifier._parse_confidence(payload.get("confidence")),
            )
        except ValueError as exc:
            raise ClassificationError(str(exc)) from exc

    @staticmethod
    def _parse_confidence(value: object) -> float | None:
        """
        Normaliza la confianza a un float en [0.0, 1.0].

        Devuelve None si el modelo no la informó o no es numérica, y recorta
        (clamp) los valores fuera de rango.
        """
        try:
            confidence = float(value)  # type: ignore[arg-type]
        except (TypeError, ValueError):
            return None
        return max(0.0, min(1.0, confidence))
