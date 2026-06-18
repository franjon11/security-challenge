"""
Test del Desafío 3 — applicant_query.sql.

Ejecuta la consulta SQL *real* (sin modificarla) contra una base SQLite en
memoria. Valida la lógica de la query (joins, filtro de 'failure', umbral > 3 y
orden descendente); no reemplaza correrla en MySQL 8.x, pero da cobertura
automática y portable sin levantar un servidor.

Requiere SQLite con soporte de CONCAT (3.44+); de lo contrario el test se omite.
"""

import os
import sqlite3
import sys

import pytest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SQL_FILE = os.path.join(REPO_ROOT, "applicant_query.sql")

SCHEMA = """
CREATE TABLE customers (
    id INTEGER PRIMARY KEY,
    first_name TEXT,
    last_name TEXT
);
CREATE TABLE campaigns (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    name TEXT
);
CREATE TABLE events (
    dt TEXT,
    campaign_id INTEGER,
    status TEXT
);
"""


def _connection() -> sqlite3.Connection:
    """Crea una conexión en memoria con el esquema del enunciado."""
    con = sqlite3.connect(":memory:")
    con.executescript(SCHEMA)
    return con


def _supports_concat(con: sqlite3.Connection) -> bool:
    try:
        con.execute("SELECT CONCAT('a', 'b')").fetchone()
        return True
    except sqlite3.OperationalError:
        return False


def _run_query(con: sqlite3.Connection) -> list[tuple]:
    """Ejecuta el archivo applicant_query.sql tal cual y devuelve las filas."""
    with open(SQL_FILE, encoding="utf-8") as fh:
        query = fh.read()
    return con.execute(query).fetchall()


def _add_failures(con: sqlite3.Connection, campaign_id: int, count: int) -> None:
    """Inserta `count` eventos 'failure' para una campaña dada."""
    con.executemany(
        "INSERT INTO events (dt, campaign_id, status) VALUES (?, ?, 'failure')",
        [(f"2021-12-01 0{i % 9}:00:00", campaign_id) for i in range(count)],
    )


def test_data_de_ejemplo_del_enunciado():
    """Con la data exacta del enunciado debe devolver solo 'Whitney Ferrero 6'."""
    con = _connection()
    if not _supports_concat(con):
        pytest.skip("Esta versión de SQLite no soporta CONCAT")

    con.executescript(
        """
        INSERT INTO customers (id, first_name, last_name) VALUES
            (1, 'Whitney', 'Ferrero'),
            (2, 'Dickie', 'Romera');
        INSERT INTO campaigns (id, customer_id, name) VALUES
            (1, 1, 'Upton Group'),
            (2, 1, 'Roob, Hudson and Rippin'),
            (3, 1, 'McCullough, Rempel and Larson'),
            (4, 1, 'Lang and Sons'),
            (5, 2, 'Ruecker, Hand and Haley');
        INSERT INTO events (dt, campaign_id, status) VALUES
            ('2021-12-02 13:52:00', 1, 'failure'),
            ('2021-12-02 08:17:48', 2, 'failure'),
            ('2021-12-02 08:18:17', 2, 'failure'),
            ('2021-12-01 11:55:32', 3, 'failure'),
            ('2021-12-01 06:53:16', 4, 'failure'),
            ('2021-12-02 04:51:09', 4, 'failure'),
            ('2021-12-01 06:34:04', 5, 'failure'),
            ('2021-12-02 03:21:18', 5, 'failure'),
            ('2021-12-01 03:18:24', 5, 'failure'),
            ('2021-12-02 15:32:37', 1, 'success'),
            ('2021-12-01 04:23:20', 1, 'success'),
            ('2021-12-02 08:01:02', 2, 'success');
        """
    )

    assert _run_query(con) == [("Whitney Ferrero", 6)]


def test_umbral_mayor_a_3_y_orden_descendente():
    """Solo aparecen clientes con > 3 fallas, ordenados de mayor a menor."""
    con = _connection()
    if not _supports_concat(con):
        pytest.skip("Esta versión de SQLite no soporta CONCAT")

    con.executescript(
        """
        INSERT INTO customers (id, first_name, last_name) VALUES
            (1, 'Ana', 'Uno'),
            (2, 'Beto', 'Dos'),
            (3, 'Caro', 'Tres');
        INSERT INTO campaigns (id, customer_id, name) VALUES
            (1, 1, 'c1'), (2, 2, 'c2'), (3, 3, 'c3');
        """
    )
    _add_failures(con, campaign_id=1, count=5)  # Ana: 5  -> incluida
    _add_failures(con, campaign_id=2, count=4)  # Beto: 4 -> incluida
    _add_failures(con, campaign_id=3, count=3)  # Caro: 3 -> excluida (no es > 3)

    assert _run_query(con) == [("Ana Uno", 5), ("Beto Dos", 4)]


def test_ignora_eventos_que_no_son_failure():
    """Los eventos 'success' no deben contarse."""
    con = _connection()
    if not _supports_concat(con):
        pytest.skip("Esta versión de SQLite no soporta CONCAT")

    con.executescript(
        """
        INSERT INTO customers (id, first_name, last_name) VALUES (1, 'Ana', 'Uno');
        INSERT INTO campaigns (id, customer_id, name) VALUES (1, 1, 'c1');
        INSERT INTO events (dt, campaign_id, status) VALUES
            ('2021-12-01 01:00:00', 1, 'failure'),
            ('2021-12-01 02:00:00', 1, 'failure'),
            ('2021-12-01 03:00:00', 1, 'failure'),
            ('2021-12-01 04:00:00', 1, 'failure'),
            ('2021-12-01 05:00:00', 1, 'success'),
            ('2021-12-01 06:00:00', 1, 'success');
        """
    )
    # 4 failures (> 3) -> aparece con 4, ignorando los 2 success.
    assert _run_query(con) == [("Ana Uno", 4)]
