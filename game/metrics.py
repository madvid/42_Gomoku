from __future__ import annotations
from typing import List, Tuple, NamedTuple
import numpy as np
from numpy import ndarray

BLACK = 1
WHITE = -1

Position = Tuple[int, int] # The indexing of positions follows numpy's one (height,width)

def swap_position(pos):
    return (pos[1], pos[0])

Row = NamedTuple('Row', [('lenght', int), ('position', Position)])
Column = NamedTuple('Column', [('lenght', int), ('position', Position)])
Diagonal = NamedTuple('Diagonal', [('lenght', int), ('position', Position)])

# Row = Tuple[int, Position]
# Column = Tuple[int, Position]
# Diagonal = Tuple[int, Position]

def measure_row(grid: ndarray, color: int) -> List[Row]:
    rows = []
    height,width = grid.shape
    for i, r in enumerate(grid):
        len_ = 0
        start_i, start_j = i, 0
        for j, x in enumerate(r):
            if x == color:
                len_ += 1
                if len_ > 1 and j == width-1:
                    rows.append(Row(len_, (start_i, start_j)))
                    len_ = 0
            else:
                if len_ < 2:
                    start_j += 1
                    len_ = 0
                else:
                    rows.append(Row(len_, (start_i, start_j)))
                    len_ = 0
                    start_i, start_j = i, j+1
    return rows

def measure_col(grid: ndarray, color: int) -> int:
    # Transpose the cols as rows to measure it
    cols_as_rows = measure_row(grid.T, color)
    # Swap position to get it right
    cols = [Column(l, swap_position(pos)) for l, pos in cols_as_rows]
    return cols
    

def measure_diag(grid: ndarray, color: int) -> int:
    max_len = 0
    for d in range(len(grid)):
        len_ = 0
        for i in range(d, len(grid)):
            for j in range(d, len(grid)):
                if grid[d+i, d+j] == color:
                    len_ += 1
                    max_len = len_ if len_ > max_len else max_len
                else:
                    len_ = 0
    return max_len    


# def measure_row(grid: ndarray, color: int) -> int:
#     max_len = 0
#     for r in grid:
#         len_ = 0
#         for i in r:
#             if i == color:
#                 len_ += 1
#                 max_len = len_ if len_ > max_len else max_len
#             else:
#                 len_ = 0
#     return max_len    

# def measure_col(grid: ndarray, color: int) -> int:
#     return measure_row(grid.T, color)

# def measure_diag(grid: ndarray, color: int) -> int:
#     max_len = 0
#     for d in range(len(grid)):
#         len_ = 0
#         for i in range(d, len(grid)):
#             for j in range(d, len(grid)):
#                 if grid[d+i, d+j] == color:
#                     len_ += 1
#                     max_len = len_ if len_ > max_len else max_len
#                 else:
#                     len_ = 0
#     return max_len    

def stone_sum(grid: ndarray, color: int) -> int:
    # Returns the difference between the total of black and white stones. The bigger the better.
    return grid.sum() * color

def longest_line(grid: ndarray, color: int) -> int:
    # Returns the difference between the longest black and white lines of stones. The bigger the better. 
    black_max = max([measure_row(grid, BLACK), measure_col(grid, BLACK), measure_diag(grid, BLACK)])
    white_max = max([measure_row(grid, WHITE), measure_col(grid, WHITE), measure_diag(grid, WHITE)])
    if color == BLACK:
        return black_max - white_max
    return white_max - black_max