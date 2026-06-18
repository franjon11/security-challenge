"""Tests de la utilidad de reintentos con backoff (escritos antes de la impl.)."""

import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from challenge_4_classification_engine.retry import call_with_retries  # noqa: E402


class _Boom(Exception):
    pass


class _Other(Exception):
    pass


def test_exito_al_primer_intento_no_duerme():
    sleeps: list[float] = []
    result = call_with_retries(lambda: 42, sleep=sleeps.append)
    assert result == 42
    assert sleeps == []


def test_reintenta_y_finalmente_tiene_exito():
    calls = {"n": 0}
    sleeps: list[float] = []

    def flaky():
        calls["n"] += 1
        if calls["n"] < 3:
            raise _Boom("falla temporal")
        return "ok"

    result = call_with_retries(
        flaky, max_attempts=3, base_delay=0.5, retryable=(_Boom,), sleep=sleeps.append
    )
    assert result == "ok"
    assert calls["n"] == 3
    # Backoff exponencial: 0.5, 1.0 entre los 3 intentos.
    assert sleeps == [0.5, 1.0]


def test_agota_intentos_y_relanza():
    sleeps: list[float] = []

    def always_fail():
        raise _Boom("siempre falla")

    with pytest.raises(_Boom):
        call_with_retries(
            always_fail, max_attempts=3, retryable=(_Boom,), sleep=sleeps.append
        )
    # Duerme entre intentos, no después del último.
    assert len(sleeps) == 2


def test_excepcion_no_retryable_se_relanza_de_inmediato():
    sleeps: list[float] = []

    def fail_other():
        raise _Other("no se reintenta")

    with pytest.raises(_Other):
        call_with_retries(
            fail_other, max_attempts=3, retryable=(_Boom,), sleep=sleeps.append
        )
    assert sleeps == []
