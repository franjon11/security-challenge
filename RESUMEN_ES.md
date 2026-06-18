# Mercado Libre — Challenge Técnico DataSec (Sr. Cybersecurity)

> Resumen en español de los puntos clave del enunciado original
> (`Mercado_Libre_DataSec_Challenge_EN.pdf`).

## Reglas generales

- **Un archivo por desafío**, con el **nombre de archivo exacto** indicado.
- Subir todo a **un único repositorio público de GitHub**.
- Lenguajes:
  - **Desafíos 1 y 2:** Python **3.12** (indicar la versión en comentarios del código).
  - **Desafío 3:** SQL puro, sintaxis **MySQL 8.x**.
  - **Desafío 4:** el lenguaje que indique el evaluador (documento aparte). *Acá usamos Python.*
- **Desafíos 1–3:** hay que respetar **exactamente** las firmas de función, nombres, parámetros
  y tipos de retorno. El código se testea de forma automática con esas firmas.
- Se pueden agregar features extra para destacar, **siempre que no rompan** la funcionalidad ni
  las firmas exigidas.
- **Desafío 4** es abierto (open-ended): el diseño es parte de lo que se evalúa.

---

## 1. Buscaminas — Conteo de minas vecinas

- **Archivo:** `solution_minesweeper.py`
- **Firma exacta:** `def count_neighbouring_mines(board: list) -> list:`
- **Entrada:** matriz 2D donde `0` = celda vacía y `1` = mina.
- **Salida:** matriz de las mismas dimensiones donde cada celda contiene la **cantidad de minas
  vecinas (0–8)**, o **`9`** si la celda es una mina.
- Cada celda tiene hasta 8 vecinos (incluye diagonales).

**Ejemplo:**

```
Entrada                Salida
[0,1,0,0]              [1,9,2,1]
[0,0,1,0]      ->      [2,3,9,2]
[0,1,0,1]              [3,9,4,9]
[1,1,0,0]              [9,9,3,1]
```

---

## 2. REST API — Mejor serie por género

- **Archivo:** `solution_best_in_genre.py`
- **Firma exacta:** `def bestInGenre(genre: str) -> str:`
- **API:** `https://jsonmock.hackerrank.com/api/tvseries` (paginada con `?page={num}`).
- **Tarea:** dado un género, devolver la serie con mayor `imdb_rating`.
- **Reglas:**
  - Empate → se devuelve el nombre **alfabéticamente menor**.
  - El match de género es **case-insensitive**.
  - Una serie puede tener **varios géneros** separados por coma.
- **Ejemplo:** `Action` → `Game of Thrones` (9.3).

---

## 3. SQL — Reporte de fallas del sistema de publicidad

- **Archivo:** `applicant_query.sql` (MySQL 8.x, SQL puro).
- **Tarea:** listar los clientes con **más de 3 eventos** con `status = 'failure'` en sus campañas,
  mostrando nombre del cliente y cantidad de fallas.
- **Orden:** por cantidad de fallas **descendente**.
- **Formato de salida:** columnas `customer`, `failures` (ej.: `Whitney Ferrero  6`).
- **Tablas:** `customers (id, first_name, last_name)`,
  `campaigns (id, customer_id, name)`,
  `events (dt, campaign_id, status)`.

---

## 4. Motor de clasificación de datos con IA

- **Archivo/estructura:** abierto (ver carpeta `challenge_4_classification_engine/`).
- **Tarea:** construir un motor que use un **LLM compatible con OpenAI** para clasificar
  textos cortos por **sensibilidad, categoría o riesgo**.
- Se hace una **demo en vivo** contra un endpoint LLM real → traer una **API key de OpenRouter**
  (o compatible).

---

## Mapa de entregables en este repo

| Desafío | Archivo / carpeta | Estado |
|--------|-------------------|--------|
| 1 | `solution_minesweeper.py` | ✅ |
| 2 | `solution_best_in_genre.py` | ✅ |
| 3 | `applicant_query.sql` | ✅ |
| 4 | `challenge_4_classification_engine/` | ✅ |
| Tests | `tests/` y `challenge_4_classification_engine/tests/` | ✅ |
