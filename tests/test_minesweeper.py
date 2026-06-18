"""Tests para el Desafío 1 — Buscaminas (Python 3.12)."""

import os
import sys

# Permite importar los módulos de solución que están en la raíz del repo.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from solution_minesweeper import count_neighbouring_mines  # noqa: E402


def test_ejemplo_del_enunciado():
    board = [
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 1, 0, 1],
        [1, 1, 0, 0],
    ]
    expected = [
        [1, 9, 2, 1],
        [2, 3, 9, 2],
        [3, 9, 4, 9],
        [9, 9, 3, 1],
    ]
    assert count_neighbouring_mines(board) == expected


def test_tablero_sin_minas():
    board = [[0, 0], [0, 0]]
    assert count_neighbouring_mines(board) == [[0, 0], [0, 0]]


def test_tablero_todo_minas():
    board = [[1, 1], [1, 1]]
    assert count_neighbouring_mines(board) == [[9, 9], [9, 9]]


def test_una_sola_celda():
    assert count_neighbouring_mines([[0]]) == [[0]]
    assert count_neighbouring_mines([[1]]) == [[9]]


def test_tablero_vacio():
    assert count_neighbouring_mines([]) == []


def test_no_muta_la_entrada():
    board = [[0, 1], [1, 0]]
    original = [row[:] for row in board]
    count_neighbouring_mines(board)
    assert board == original
