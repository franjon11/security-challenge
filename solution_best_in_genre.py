"""
Desafío 2 — REST API: mejor serie de TV por género.

Lenguaje: Python 3.12

Consulta la API paginada https://jsonmock.hackerrank.com/api/tvseries y devuelve
el nombre de la serie con mayor imdb_rating dentro de un género dado. Ante empate,
devuelve el nombre alfabéticamente menor.

Se usa únicamente la librería estándar (urllib + json) para no depender de paquetes
externos en el entorno de testeo automático.
"""

import json
from urllib.request import urlopen

API_URL = "https://jsonmock.hackerrank.com/api/tvseries"
_REQUEST_TIMEOUT_SECONDS = 10


def _fetch_page(page: int) -> dict:
    """
    Descarga una página de la API y la devuelve como diccionario.

    Se aísla la llamada HTTP en una función propia para poder mockearla
    fácilmente en los tests (sin tocar la red real).

    Parameters:
        page (int): número de página a solicitar (1-indexado).

    Returns:
        dict: respuesta JSON parseada de la API.
    """
    url = f"{API_URL}?page={page}"
    with urlopen(url, timeout=_REQUEST_TIMEOUT_SECONDS) as response:
        return json.loads(response.read().decode("utf-8"))


def _matches_genre(show: dict, genre: str) -> bool:
    """
    Indica si la serie pertenece al género buscado.

    El campo `genre` puede contener varios géneros separados por coma; la
    comparación es case-insensitive y tolerante a espacios.

    Parameters:
        show (dict): registro de la serie devuelto por la API.
        genre (str): género buscado, ya normalizado a minúsculas.

    Returns:
        bool: True si la serie incluye el género buscado.
    """
    raw_genres = show.get("genre", "") or ""
    show_genres = {g.strip().lower() for g in raw_genres.split(",")}
    return genre in show_genres


def _rating_of(show: dict) -> float:
    """
    Devuelve el imdb_rating de la serie como float (0.0 si no es válido).

    Parameters:
        show (dict): registro de la serie devuelto por la API.

    Returns:
        float: rating numérico de la serie.
    """
    try:
        return float(show.get("imdb_rating"))
    except (TypeError, ValueError):
        return 0.0


def bestInGenre(genre: str) -> str:
    """
    Finds the highest-rated TV series in the given genre.

    Parameters:
        genre (str): The genre to search for (e.g., 'Action', 'Comedy', 'Drama')

    Returns:
        str: The name of the highest-rated show in the genre. If there is a tie,
             returns the alphabetically lower name. Returns the name as a string.

    Notes:
        - Ties are broken by alphabetical order of the show name
        - Genre matching is case-insensitive
        - Shows can have multiple genres (comma-separated)
    """
    target_genre = genre.strip().lower()

    best_name: str | None = None
    best_rating = float("-inf")

    page = 1
    total_pages = 1  # Se actualiza con el valor real tras la primera página.
    while page <= total_pages:
        payload = _fetch_page(page)
        total_pages = payload.get("total_pages", page)

        for show in payload.get("data", []):
            if not _matches_genre(show, target_genre):
                continue

            rating = _rating_of(show)
            name = show.get("name", "")

            # Gana mayor rating; ante empate, el nombre alfabéticamente menor.
            is_better = rating > best_rating
            is_tie_break = rating == best_rating and (
                best_name is None or name < best_name
            )
            if is_better or is_tie_break:
                best_rating = rating
                best_name = name

        page += 1

    return best_name if best_name is not None else ""


if __name__ == "__main__":
    # Ejecución rápida contra la API real.
    print(bestInGenre("Action"))
