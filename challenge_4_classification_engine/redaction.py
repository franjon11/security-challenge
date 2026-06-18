"""
Redacción de datos sensibles para logging.

Antes de registrar un texto en los logs se enmascaran patrones potencialmente
sensibles (tarjetas, documentos, emails, tokens). Así el motor puede dejar
trazas útiles sin filtrar el dato que justamente está clasificando.
"""

from __future__ import annotations

import re

# Emails: usuario@dominio.tld
_EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")

# Secuencias numéricas largas: tarjetas, DNI, teléfonos (admite espacios, puntos y guiones).
_LONG_DIGITS = re.compile(r"\d[\d .\-]{6,}\d")

# Tokens / secretos: cadenas alfanuméricas largas (api keys, hashes, etc.).
_TOKEN = re.compile(r"\b[A-Za-z0-9_-]{20,}\b")


def redact(text: str) -> str:
    """
    Devuelve el texto con los datos sensibles enmascarados.

    El orden importa: primero emails, luego tokens largos y por último las
    secuencias numéricas, para que [NUM] no fragmente un token antes de tiempo.

    Parameters:
        text (str): texto original.

    Returns:
        str: texto con marcadores [EMAIL], [TOKEN] y [NUM] en lugar de los datos.
    """
    text = _EMAIL.sub("[EMAIL]", text)
    text = _TOKEN.sub("[TOKEN]", text)
    text = _LONG_DIGITS.sub("[NUM]", text)
    return text
