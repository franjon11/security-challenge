"""
Desafío 1 — Buscaminas: conteo de minas vecinas.

Lenguaje: Python 3.12

Dada una matriz de Buscaminas (0 = vacío, 1 = mina), devuelve otra matriz de las
mismas dimensiones donde cada celda contiene la cantidad de minas adyacentes (0-8),
o 9 si la celda es una mina.
"""

# Desplazamientos de las 8 celdas vecinas (incluye diagonales).
# Se define una sola vez como constante para no recalcularlo por celda.
_NEIGHBOUR_OFFSETS: tuple[tuple[int, int], ...] = (
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),           (0, 1),
    (1, -1),  (1, 0),  (1, 1),
)

MINE = 1
MINE_OUTPUT = 9


def _count_mines_around(board: list, row: int, col: int) -> int:
    """
    Cuenta cuántas minas hay en las celdas vecinas de (row, col).

    Parameters:
        board (list): tablero de entrada (0 = vacío, 1 = mina).
        row (int): índice de fila de la celda a evaluar.
        col (int): índice de columna de la celda a evaluar.

    Returns:
        int: cantidad de minas vecinas (0-8).
    """
    rows = len(board)
    cols = len(board[0])
    count = 0
    for d_row, d_col in _NEIGHBOUR_OFFSETS:
        n_row, n_col = row + d_row, col + d_col
        # Solo cuenta vecinos que caen dentro del tablero.
        if 0 <= n_row < rows and 0 <= n_col < cols:
            if board[n_row][n_col] == MINE:
                count += 1
    return count


def count_neighbouring_mines(board: list) -> list:
    """
    Cuenta las minas vecinas de cada celda de un tablero de Buscaminas.

    Parameters:
        board (list): lista 2D donde 0 representa un espacio vacío y 1 una mina.

    Returns:
        list: lista 2D donde cada celda contiene la cantidad de minas vecinas,
              o 9 si la celda contiene una mina.
    """
    # Tablero vacío: se devuelve tal cual (mismas dimensiones, sin celdas).
    if not board or not board[0]:
        return [row[:] for row in board]

    result: list = []
    for row_idx, row in enumerate(board):
        new_row: list = []
        for col_idx, cell in enumerate(row):
            if cell == MINE:
                new_row.append(MINE_OUTPUT)
            else:
                new_row.append(_count_mines_around(board, row_idx, col_idx))
        result.append(new_row)
    return result


if __name__ == "__main__":
    # Ejemplo del enunciado para una verificación rápida manual.
    example = [
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 1, 0, 1],
        [1, 1, 0, 0],
    ]
    for output_row in count_neighbouring_mines(example):
        print(output_row)
