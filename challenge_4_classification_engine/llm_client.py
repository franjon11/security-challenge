"""
Cliente LLM compatible con OpenAI.

Se define un Protocol (`LLMClient`) para desacoplar el motor del proveedor
concreto: el `DataClassifier` solo depende de la interfaz, no del SDK. Esto
permite inyectar un cliente falso en los tests sin tocar la red.
"""

from __future__ import annotations

from typing import Protocol

from .config import Config
from .retry import call_with_retries


class LLMClient(Protocol):
    """Interfaz mínima que el motor necesita de un proveedor LLM."""

    def complete(self, system_prompt: str, user_prompt: str) -> str:
        """
        Envía los prompts al modelo y devuelve el contenido de la respuesta.

        Parameters:
            system_prompt (str): instrucciones del sistema.
            user_prompt (str): mensaje del usuario (texto a clasificar).

        Returns:
            str: texto crudo devuelto por el modelo (se espera JSON).
        """
        ...


class OpenAICompatibleClient:
    """
    Implementación de `LLMClient` sobre el SDK oficial de OpenAI.

    Funciona con cualquier endpoint compatible (OpenRouter, OpenAI, etc.)
    configurando `base_url` y `model` en `Config`.
    """

    def __init__(self, config: Config) -> None:
        # Import diferido: el SDK solo es necesario para la demo real, no para
        # importar el paquete ni correr los tests con un cliente falso.
        from openai import OpenAI

        self._config = config
        self._client = OpenAI(
            api_key=config.api_key,
            base_url=config.base_url,
            timeout=config.timeout,
        )

    def complete(self, system_prompt: str, user_prompt: str) -> str:
        """
        Llama al endpoint de chat completions y devuelve el texto de la respuesta.

        Reintenta automáticamente ante errores transitorios (timeout, problemas
        de conexión, rate limit o errores 5xx) con backoff exponencial.
        """
        import openai

        retryable = (
            openai.APITimeoutError,
            openai.APIConnectionError,
            openai.RateLimitError,
            openai.InternalServerError,
        )
        return call_with_retries(
            lambda: self._request(system_prompt, user_prompt),
            max_attempts=self._config.max_attempts,
            base_delay=self._config.retry_base_delay,
            retryable=retryable,
        )

    def _request(self, system_prompt: str, user_prompt: str) -> str:
        """Realiza una única llamada al modelo (sin reintentos)."""
        response = self._client.chat.completions.create(
            model=self._config.model,
            temperature=self._config.temperature,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        return response.choices[0].message.content or ""
