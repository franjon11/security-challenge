"""
CLI para la demo en vivo del motor de clasificación.

Uso:
    # Clasificar un texto pasado como argumento
    python -m challenge_4_classification_engine.cli "Mi tarjeta es 4111 1111 1111 1111"

    # Clasificar varias líneas desde stdin (una por línea)
    cat muestras.txt | python -m challenge_4_classification_engine.cli

Requiere la variable de entorno LLM_API_KEY (OpenRouter o compatible).
"""

from __future__ import annotations

import argparse
import json
import logging
import sys

from .config import Config
from .engine import ClassificationError, DataClassifier
from .llm_client import OpenAICompatibleClient


def _read_inputs(args_texts: list[str]) -> list[str]:
    """
    Obtiene los textos a clasificar desde los argumentos o desde stdin.

    Parameters:
        args_texts (list[str]): textos recibidos por línea de comandos.

    Returns:
        list[str]: textos no vacíos a clasificar.
    """
    if args_texts:
        return args_texts
    # Sin argumentos: se leen líneas desde stdin (modo batch).
    return [line.strip() for line in sys.stdin if line.strip()]


def main(argv: list[str] | None = None) -> int:
    """Punto de entrada de la CLI. Devuelve el código de salida del proceso."""
    parser = argparse.ArgumentParser(
        description="Clasifica textos por sensibilidad, categoría y riesgo usando un LLM."
    )
    parser.add_argument(
        "texts",
        nargs="*",
        help="Texto(s) a clasificar. Si se omite, se lee desde stdin (una línea por texto).",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Muestra logs de progreso (con los datos sensibles redactados).",
    )
    args = parser.parse_args(argv)

    if args.verbose:
        logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    texts = _read_inputs(args.texts)
    if not texts:
        parser.error("No se recibió ningún texto para clasificar.")

    try:
        config = Config.from_env()
    except ValueError as exc:
        print(f"Error de configuración: {exc}", file=sys.stderr)
        return 2

    classifier = DataClassifier(OpenAICompatibleClient(config))

    results = []
    for text in texts:
        try:
            results.append(classifier.classify(text).to_dict())
        except ClassificationError as exc:
            results.append({"text": text, "error": str(exc)})

    # Salida en JSON para que sea fácil de leer y de integrar con otras tools.
    print(json.dumps(results, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
