# Mercado Libre — Challenge Técnico DataSec (Sr. Cybersecurity)

Soluciones a los 4 desafíos del challenge técnico.

## Estructura

```
.
├── solution_minesweeper.py        # Desafío 1 — Buscaminas
├── solution_best_in_genre.py      # Desafío 2 — REST API: mejor serie por género
├── applicant_query.sql            # Desafío 3 — SQL (MySQL 8.x)
├── challenge_4_classification_engine/   # Desafío 4 — Motor de clasificación con IA
├── tests/                         # Tests de los desafíos 1 y 2
├── requirements.txt
└── README.md
```

## Desafíos

### 1. Buscaminas — `solution_minesweeper.py`
Cuenta minas vecinas de cada celda. Firma exacta:
`def count_neighbouring_mines(board: list) -> list`.

### 2. Mejor serie por género — `solution_best_in_genre.py`
Consulta la API paginada de HackerRank y devuelve la serie con mayor `imdb_rating`
del género (desempate alfabético). Firma exacta: `def bestInGenre(genre: str) -> str`.
Usa solo librería estándar (`urllib`).

### 3. Reporte de fallas — `applicant_query.sql`
Clientes con más de 3 eventos `failure`, ordenados desc. (MySQL 8.x).

### 4. Motor de clasificación con IA — `challenge_4_classification_engine/`
Clasifica textos por sensibilidad, categoría y riesgo con un LLM compatible con
OpenAI. Ver su [README](challenge_4_classification_engine/README.md).

## Requisitos

- Python **3.12**
- Dependencias: `pip install -r requirements.txt`
  (los desafíos 1–3 corren sin dependencias externas).

## Tests

```bash
pip install -r requirements.txt
pytest
```

> Los tests de los desafíos 1, 2 y 4 corren sin red ni API key (la API y el LLM
> se mockean). El desafío 2 contra la API real se prueba con
> `python solution_best_in_genre.py`.
