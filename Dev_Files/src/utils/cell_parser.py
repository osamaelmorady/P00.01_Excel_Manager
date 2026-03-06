import re
from typing import Tuple


# -------------------------
# column / row converters
# -------------------------

def excel_col_to_index(col: str) -> int:
    col = col.upper()
    idx = 0
    for c in col:
        idx = idx * 26 + (ord(c) - ord('A') + 1)
    return idx - 1


def excel_row_to_index(row: str) -> int:
    return int(row) - 1


# -------------------------
# A1 parser
# -------------------------

CELL_RE = re.compile(r"([A-Za-z]+)(\d+)")


def cell_to_indices(cell: str) -> Tuple[int, int]:
    """
    'B3' -> (2, 1)
    """
    match = CELL_RE.fullmatch(cell.strip())
    if not match:
        raise ValueError(f"Invalid cell reference: {cell}")

    col_str, row_str = match.groups()
    return excel_row_to_index(row_str), excel_col_to_index(col_str)
