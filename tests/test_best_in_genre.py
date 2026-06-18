"""
Tests para el Desafío 2 — mejor serie por género (Python 3.12).

Se mockea `_fetch_page` para no depender de la red real y validar la lógica
de paginación, match de género, mayor rating y desempate alfabético.
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import solution_best_in_genre as sol  # noqa: E402
from solution_best_in_genre import bestInGenre  # noqa: E402


def _fake_api(pages):
    """Crea un reemplazo de `_fetch_page` a partir de una lista de páginas de data."""
    total = len(pages)

    def _fetch(page):
        return {
            "page": page,
            "total_pages": total,
            "data": pages[page - 1],
        }

    return _fetch


def test_mayor_rating_simple(monkeypatch):
    pages = [[
        {"name": "Game of Thrones", "genre": "Action, Drama", "imdb_rating": "9.3"},
        {"name": "Some Comedy", "genre": "Comedy", "imdb_rating": "9.9"},
    ]]
    monkeypatch.setattr(sol, "_fetch_page", _fake_api(pages))
    assert bestInGenre("Action") == "Game of Thrones"


def test_paginacion(monkeypatch):
    pages = [
        [{"name": "Low", "genre": "Action", "imdb_rating": "7.0"}],
        [{"name": "High", "genre": "Action", "imdb_rating": "9.5"}],
    ]
    monkeypatch.setattr(sol, "_fetch_page", _fake_api(pages))
    assert bestInGenre("Action") == "High"


def test_empate_desempata_alfabeticamente(monkeypatch):
    pages = [[
        {"name": "Zeta Show", "genre": "Drama", "imdb_rating": "9.0"},
        {"name": "Alpha Show", "genre": "Drama", "imdb_rating": "9.0"},
    ]]
    monkeypatch.setattr(sol, "_fetch_page", _fake_api(pages))
    assert bestInGenre("Drama") == "Alpha Show"


def test_genero_case_insensitive(monkeypatch):
    pages = [[
        {"name": "Mixed", "genre": "Sci-Fi, ACTION", "imdb_rating": "8.0"},
    ]]
    monkeypatch.setattr(sol, "_fetch_page", _fake_api(pages))
    assert bestInGenre("action") == "Mixed"


def test_genero_inexistente_devuelve_vacio(monkeypatch):
    pages = [[
        {"name": "Mixed", "genre": "Comedy", "imdb_rating": "8.0"},
    ]]
    monkeypatch.setattr(sol, "_fetch_page", _fake_api(pages))
    assert bestInGenre("Horror") == ""
