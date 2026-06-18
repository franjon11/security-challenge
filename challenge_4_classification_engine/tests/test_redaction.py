"""Tests de la redacción de datos sensibles para logging (test-first)."""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from challenge_4_classification_engine.redaction import redact  # noqa: E402


def test_enmascara_numero_de_tarjeta():
    out = redact("Mi tarjeta es 4111 1111 1111 1111")
    assert "4111" not in out
    assert "[NUM]" in out


def test_enmascara_dni_con_puntos():
    out = redact("DNI 30.123.456")
    assert "30.123.456" not in out
    assert "[NUM]" in out


def test_enmascara_email():
    out = redact("contacto: juan.perez@example.com")
    assert "@example.com" not in out
    assert "[EMAIL]" in out


def test_enmascara_token_largo():
    out = redact("api key: sk-or-v1-abcdef0123456789abcdef")
    assert "abcdef0123456789" not in out
    assert "[TOKEN]" in out


def test_texto_normal_no_se_modifica():
    texto = "El clima de hoy esta soleado"
    assert redact(texto) == texto
