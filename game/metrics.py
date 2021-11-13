from __future__ import annotations
from typing import List, Tuple#, NamedTuple
import numpy as np

BLACK = 1
WHITE = -1

class Position():
    def __init__(self, i, j) -> None:
        self.i = i
        self.j = j
    
    def __add__(self, p: Position) -> Position:
        return Position(self.i + p.i, self.j + p.j)
    
    def __eq__(self, o: object) -> bool:
        return self.i == o.i and self.j == o.j

    def swap(self):
        return Position(self.j, self.i)

# Position = Tuple[int, int] # The indexing of positions follows numpy's one (height,width)

# def swap_position(pos): #FIXME: should be move to utils or added to a Position class
#     return (pos[1], pos[0])


class StoneSequence():
    # Global attributes of all sequences. Generated once before building the tree.
    grid: np.ndarray = None
    max_height: int = None
    max_width: int = None

    def __init__(self, length: int, position: Position, color: int) -> None:
        self.length = length
        self.start = position
        self.end = None
        self.color = color

    def is_surrounded(self):
        raise NotImplementedError

    def __eq__(self, o: object) -> bool:
        return self.length == o.length and self.start == o.start
    # def to_row(self):
    #     return Row(self.length, self.start, self.color)

    # def to_col(self):
    #     return Column(self.length, self.start, self.color)

    # def to_diag(self, left: bool):
    #     return Diagonal(self.length, self.start, self.color, left)


class Row(StoneSequence):
    def __init__(self, length, position, color) -> None:
        super().__init__(length, position, color)
        self.end = self.start + Position(0, length)

    def is_surrounded(self):
        if (self.start[1] != 0
            and self.grid[self.start[0], self.start[1] - 1] == (self.color * -1)
            and self.end[1] != self.max_width 
            and self.grid[self.end[0], self.end[1] + 1] == (self.color * -1)):
            return True
        return False
        

class Column(StoneSequence):
    def __init__(self, length, position, color) -> None:
        super().__init__(length, position, color)
        self.end = self.start + Position(length, 0)

    def is_surrounded(self):
        if (self.start[0] != 0
            and self.grid[self.start[0] - 1, self.start[1]] == (self.color * -1)
            and self.end[0] != self.max_height 
            and self.grid[self.end[0] + 1, self.end[1]] == (self.color * -1)):
            return True
        return False


class Diagonal(StoneSequence):
    def __init__(self, length: int, position: Position, color: int, left: bool) -> None:
        super().__init__(length, position, color)
        self.left = left
        self.end = self.start + Position(length, length) #if left else self.start - Position(length, length)

    def is_surrounded(self):
        if self.left:
            if (self.start[0] != 0 and self.start[1] != 0
                and self.grid[self.start[0] - 1, self.start[1] -1] == (self.color * -1)
                and self.end[0] != self.max_height and self.end[1] != self.max_width
                and self.grid[self.end[0] + 1, self.end[1] + 1] == (self.color * -1)):
                return True
        else: 
            if (self.start[0] != 0 and self.start[1] != self.max_height
                and self.grid[self.start[0] - 1, self.start[1] + 1] == (self.color * -1)
                and self.end[0] != self.max_height and self.end[1] != 0
                and self.grid[self.end[0] + 1, self.end[1] - 1] == (self.color * -1)):
                return True
        return False


# Row = NamedTuple('Row', [('lenght', int), ('position', Position)])
# Column = NamedTuple('Column', [('lenght', int), ('position', Position)])
# Diagonal = NamedTuple('Diagonal', [('lenght', int), ('position', Position), ('left', bool)])

# Row = Tuple[int, Position]
# Column = Tuple[int, Position]
# Diagonal = Tuple[int, Position]

def measure_sequence(grid: np.ndarray, color: int) -> List[StoneSequence]:
    seqs = []
    for i, r in enumerate(grid):
        len_ = 0
        start_i, start_j = i, 0
        # For each sequence, count the number n of consecutive stones of the same color. If n > 2, the row is registered.
        for j, x in enumerate(r):
            # Correct color found.
            if x == color:
                len_ += 1
                # Case: end of line
                if len_ > 1 and j == len(r)-1:
                    seqs.append(StoneSequence(len_, Position(start_i, start_j), color))
                    len_ = 0
            # Incorrect color.
            else:
                if len_ < 2:
                    start_j = j+1
                    len_ = 0
                else:
                    seqs.append(StoneSequence(len_, Position(start_i, start_j), color))
                    len_ = 0
                    start_i, start_j = i, j+1
    return seqs

def measure_row(grid: np.ndarray, color: int) -> List[Row]:
    sequences = measure_sequence(grid, color)
    return [Row(seq.length, seq.start, seq.color) for seq in sequences]

def measure_col(grid: np.ndarray, color: int) -> List[Column]:
    # Transpose the cols as rows to measure it
    cols_sequences = measure_sequence(grid.T, color)
    # Swap position to get it right
    cols = [Column(seq.length, seq.start.swap(), seq.color) for seq in cols_sequences]
    return cols

def convert_to_pos(d_pos: Position, i_max: int, left: bool = True) -> Position:
    d_i, d_j = d_pos.i, d_pos.j
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
        return Position(i, j)
    else:
        return Position(i, i_max - j) 

def measure_diag(grid: np.ndarray, color: int) -> List[Diagonal]:
    i_max = grid.shape[0] - 1
    l_diags_lst = [np.diag(grid, k=n) for n in range(-grid.shape[0]+1, grid.shape[1])]
    r_diags_lst = [np.diag(np.fliplr(grid), k=n) for n in range(-grid.shape[0]+1, grid.shape[1])]
    
    l_diags_as_row = measure_sequence(l_diags_lst, color)
    r_diags_as_row = measure_sequence(r_diags_lst, color)

    l_diags = [Diagonal(seq.length, convert_to_pos(seq.start, i_max, left=True),  seq.color,  left=True) for seq in l_diags_as_row]
    r_diags = [Diagonal(seq.length, convert_to_pos(seq.start, i_max, left=False), seq.color, left=False) for seq in r_diags_as_row]
    
    return l_diags + r_diags

# def measure_row(grid: np.ndarray, color: int) -> List[Row]:
#     rows = []
#     # _, width = grid.shape
#     for i, r in enumerate(grid):
#         len_ = 0
#         start_i, start_j = i, 0
#         # For each row, count the number n of consecutive stones of the same color. If n > 2, the row is registered.
#         for j, x in enumerate(r):
#             # Correct color found.
#             if x == color:
#                 len_ += 1
#                 # Case: end of line
#                 if len_ > 1 and j == len(r)-1:
#                     rows.append(Row(len_, Position(start_i, start_j), color))
#                     len_ = 0
#             # Incorrect color.
#             else:
#                 if len_ < 2:
#                     start_j = j+1
#                     len_ = 0
#                 else:
#                     rows.append(Row(len_, Position(start_i, start_j), color))
#                     len_ = 0
#                     start_i, start_j = i, j+1
#     return rows


    



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