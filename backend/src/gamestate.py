from collections import namedtuple, Counter
from typing import List

Turns = namedtuple("Turns", ["x", "o"])


def get_turns(board) -> Turns:
    flattened_board = [point for row in board for point in row]
    counts = dict(Counter(flattened_board))
    return Turns(counts["x"], counts["o"])


def get_columns(board) -> List[List[str]]:
    return [[row[i] for row in board] for i in range(len(board))]


def get_first_diagonals(board) -> List[List[str]]:
    def extract_diagonal(start_row: int, start_col: int) -> List[str]:
        # extract a diagonal starting from (start_row, start_col)
        diagonal = []
        row, col = start_row, start_col
        while row < rows_count and col < cols_count:
            diagonal.append(board[row][col])
            row += 1
            col += 1
        return diagonal

    rows_count, cols_count = len(board), len(board[0])
    diagonals = []

    for col_start in range(cols_count):
        diagonals.append(extract_diagonal(0, col_start))

    for row_start in range(1, rows_count):
        diagonals.append(extract_diagonal(row_start, 0))

    return diagonals


def get_second_diagonals(board) -> List[List[str]]:
    transposed_board = get_columns(board)[::-1]  # turn the board by 90 degrees

    return get_first_diagonals(transposed_board)


# sliding window

# if only one item in counter
# and numbeer count > 4
# endgame


def process_single_sequence(sequence: List[str], winning_length):
    """
    Look up endgame patterns with a sliding window

    Returns True if an endgame pattern was found
    """

    if winning_length > len(sequence):
        return False

    start, end = 0, winning_length

    while end < len(sequence):
        window = sequence[start:end]
        window_counter = Counter(window)
        del window_counter[""]

        if any(count >= 4 for count in window_counter.values()):
            return True
        start += 1
        end += 1
    return False


def process_direction(direction, winning_length):
    """
    Look up endgame patterns for each sequence in a given direction

    Returns True if an endgame pattern was found
    """
    for sequence in direction:
        if process_single_sequence(sequence, winning_length):
            return True
    return False


def is_endgame(board, winning_length):
    """
    Args:
        board: gameboard 2d list representation
        winning_length: character streak length required to win

    Determine if board is in an endgame state
    Returns True if an endgame pattern was found
    """
    directions = [
        board,
        get_columns(board),
        get_first_diagonals(board),
        get_second_diagonals(board),
    ]

    for d in directions:
        if process_direction(d, winning_length):
            return True
    return False


def get_gamestate(board) -> str:
    if is_endgame(board):
        return "endgame"

    if max(get_turns(board)) < 6:
        return "opening"

    return "midgame"
