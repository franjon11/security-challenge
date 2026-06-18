"""
Utilidad de reintentos con backoff exponencial.

Se mantiene genérica e independiente del proveedor LLM para poder testearla en
aislamiento (inyectando `sleep`) sin esperar tiempos reales ni tocar la red.
"""

from __future__ import annotations

import time
from typing import Callable, TypeVar

T = TypeVar("T")


def call_with_retries(
    func: Callable[[], T],
    *,
    max_attempts: int = 3,
    base_delay: float = 0.5,
    retryable: tuple[type[Exception], ...] = (Exception,),
    sleep: Callable[[float], None] = time.sleep,
) -> T:
    """
    Ejecuta `func` reintentando ante excepciones retryables con backoff exponencial.

    Parameters:
        func: callable sin argumentos a ejecutar.
        max_attempts: cantidad máxima de intentos (incluye el primero).
        base_delay: espera base en segundos; crece como base_delay * 2**(intento-1).
        retryable: tupla de excepciones que disparan reintento. Cualquier otra
                   excepción se propaga de inmediato.
        sleep: función de espera (inyectable para tests).

    Returns:
        El valor devuelto por `func`.

    Raises:
        La última excepción si se agotan los intentos, o cualquier excepción
        no incluida en `retryable`.
    """
    last_exc: Exception | None = None
    for attempt in range(1, max_attempts + 1):
        try:
            return func()
        except retryable as exc:
            last_exc = exc
            if attempt == max_attempts:
                break
            sleep(base_delay * (2 ** (attempt - 1)))
    assert last_exc is not None  # garantizado: solo se sale del loop tras una excepción
    raise last_exc
