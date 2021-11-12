from __future__ import annotations
from typing import List, Tuple, NamedTuple
import numpy as np

BLACK = 1
WHITE = -1

Position = Tuple[int, int] # The indexing of positions follows numpy's one (height,width)

def swap_position(pos): #FIXME: should be move to utils or added to a Position class
    return (pos[1], pos[0])

Row = NamedTuple('Row', [('lenght', int), ('position', Position)])
Column = NamedTuple('Column', [('lenght', int), ('position', Position)])
Diagonal = NamedTuple('Diagonal', [('lenght', int), ('position', Position), ('left', bool)])

# Row = Tuple[int, Position]
# Column = Tuple[int, Position]
# Diagonal = Tuple[int, Position]

def measure_row(grid: np.ndarray, color: int) -> List[Row]:
    rows = []
    # _, width = grid.shape
    for i, r in enumerate(grid):
        len_ = 0
        start_i, start_j = i, 0
        # For each row, count the number n of consecutive stones of the same color. If n > 2, the row is registered.
        for j, x in enumerate(r):
            # Correct color found.
            if x == color:
                len_ += 1
                # Case: end of line
                if len_ > 1 and j == len(r)-1:
                    rows.append(Row(len_, (start_i, start_j)))
                    len_ = 0
            # Incorrect color.
            else:
                if len_ < 2:
                    start_j = j+1
                    len_ = 0
                else:
                    rows.append(Row(len_, (start_i, start_j)))
                    len_ = 0
                    start_i, start_j = i, j+1
    return rows

def measure_col(grid: np.ndarray, color: int) -> List[Column]:
    # Transpose the cols as rows to measure it
    cols_as_rows = measure_row(grid.T, color)
    # Swap position to get it right
    cols = [Column(l, swap_position(pos)) for l, pos in cols_as_rows]
    return cols
    
def convert_to_pos(d_pos: Position, i_max: int, left: bool = True) -> Position:
    d_i, d_j = d_pos
    # Convert to the proper position of the diagonal.
    # The position of the diagonal correspond to the 'uppest' stone on the board,
    # (i.e. the smallest value of col row index).
    if d_i < i_max:
        i = i_max - d_i + d_j
        j = d_j
    elif d_i == i_max:
        i = d_j
        j = d_j
    else:
        i = d_j
        j = d_i - i_max + d_j
        
    # If the diagonal start from the right, flip the row index.
    if left: 
        return (i, j)
    else:
        return (i, i_max - j) 

def measure_diag(grid: np.ndarray, color: int) -> List[Diagonal]:
    i_max = grid.shape[0] - 1
    l_diags_lst = [np.diag(grid, k=n) for n in range(-grid.shape[0]+1, grid.shape[1])]
    r_diags_lst = [np.diag(np.fliplr(grid), k=n) for n in range(-grid.shape[0]+1, grid.shape[1])]
    
    l_diags_as_row = measure_row(l_diags_lst, color)
    r_diags_as_row = measure_row(r_diags_lst, color)

    l_diags = [Diagonal(l, convert_to_pos(pos, i_max, left=True), left=True ) for l, pos in l_diags_as_row]
    r_diags = [Diagonal(l, convert_to_pos(pos, i_max, left=False), left=False) for l, pos in r_diags_as_row]
    
    return l_diags + r_diags

def stone_sum(grid: np.ndarray, color: int) -> int:
    # Returns the difference between the total of black and white stones. The bigger the better.
    return grid.sum() * color

def longest_line(grid: np.ndarray, color: int) -> int:
    # Returns the difference between the longest black and white lines of stones. The bigger the better. 
    black_max = max([measure_row(grid, BLACK), measure_col(grid, BLACK), measure_diag(grid, BLACK)])
    white_max = max([measure_row(grid, WHITE), measure_col(grid, WHITE), measure_diag(grid, WHITE)])
    if color == BLACK:
        return black_max - white_max
    return white_max - black_max