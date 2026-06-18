"""Tests de la configuración: lectura de entorno y reintentos (test-first)."""

import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from challenge_4_classification_engine.config import Config  # noqa: E402


def test_from_env_lee_variables(monkeypatch):
    monkeypatch.setenv("LLM_API_KEY", "secreta")
    monkeypatch.setenv("LLM_MODEL", "openai/gpt-4o")
    monkeypatch.setenv("LLM_MAX_ATTEMPTS", "5")
    config = Config.from_env()
    assert config.api_key == "secreta"
    assert config.model == "openai/gpt-4o"
    assert config.max_attempts == 5


def test_from_env_sin_api_key_falla(monkeypatch):
    monkeypatch.delenv("LLM_API_KEY", raising=False)
    with pytest.raises(ValueError):
        Config.from_env()


def test_defaults_de_reintentos(monkeypatch):
    monkeypatch.setenv("LLM_API_KEY", "secreta")
    monkeypatch.delenv("LLM_MAX_ATTEMPTS", raising=False)
    config = Config.from_env()
    assert config.max_attempts == 3
    assert config.retry_base_delay > 0
