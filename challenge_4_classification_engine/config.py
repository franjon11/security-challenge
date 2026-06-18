"""
Configuración del motor de clasificación.

Centraliza los parámetros de conexión al LLM. Por defecto apunta a OpenRouter
(endpoint compatible con OpenAI), pero sirve para cualquier proveedor que
exponga la API de OpenAI cambiando `base_url` y `model`.
"""

from __future__ import annotations

import os
from dataclasses import dataclass

# OpenRouter expone una API compatible con OpenAI.
DEFAULT_BASE_URL = "https://openrouter.ai/api/v1"
DEFAULT_MODEL = "openai/gpt-4o-mini"


@dataclass(frozen=True)
class Config:
    """
    Parámetros de conexión y comportamiento del cliente LLM.

    Attributes:
        api_key: clave de API del proveedor (obligatoria para la demo en vivo).
        base_url: endpoint compatible con OpenAI.
        model: identificador del modelo a usar.
        temperature: baja por defecto para que la clasificación sea determinista.
        timeout: tiempo máximo de espera por respuesta, en segundos.
    """

    api_key: str
    base_url: str = DEFAULT_BASE_URL
    model: str = DEFAULT_MODEL
    temperature: float = 0.0
    timeout: float = 30.0

    @classmethod
    def from_env(cls) -> "Config":
        """
        Construye la configuración a partir de variables de entorno.

        Variables soportadas:
            LLM_API_KEY        (obligatoria)
            LLM_BASE_URL       (opcional, default OpenRouter)
            LLM_MODEL          (opcional)
            LLM_TEMPERATURE    (opcional)

        Raises:
            ValueError: si falta la API key.
        """
        api_key = os.environ.get("LLM_API_KEY", "").strip()
        if not api_key:
            raise ValueError(
                "Falta la variable de entorno LLM_API_KEY. "
                "Exportá tu API key de OpenRouter (o compatible) antes de correr la demo."
            )
        return cls(
            api_key=api_key,
            base_url=os.environ.get("LLM_BASE_URL", DEFAULT_BASE_URL),
            model=os.environ.get("LLM_MODEL", DEFAULT_MODEL),
            temperature=float(os.environ.get("LLM_TEMPERATURE", "0.0")),
        )
