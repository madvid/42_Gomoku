from __future__ import annotations
from typing import List, Tuple
import numpy as np

BLACK = 1
WHITE = -1

class Position():
    def __init__(self, i, j) -> None:
        self.i = i
        self.j = j
    
    def __add__(self, p: Position) -> Position:
        return Position(self.i + p.i, self.j + p.j)
    
    def __sub__(self, p: Position) -> Position:
        return Position(self.i - p.i, self.j - p.j)

    def __eq__(self, o: object) -> bool:
        return self.i == o.i and self.j == o.j
    
    def __repr__(self) -> str:
        return f"({self.i}, {self.j})"

    def __getitem__(self, key: int) -> int:
        if key == 0:
            return self.i
        elif key == 1:
            return self.j
        else:
            raise KeyError

    def swap(self):
        return Position(self.j, self.i)


class StoneSequence():
    def __init__(self, length: int, position: Position, color: int, grid: np.ndarray) -> None:
        self.length = length
        self.start = position
        self.color = color
        self.grid = grid
        
        # Attributes updated in the child classes
        self.end = None
        self.distance_to_edge = None

    def _previous_idx(self, distance: int) -> Tuple[int, int]:
        raise NotImplementedError
    
    def _next_idx(self, distance: int) -> Tuple[int, int]:
        raise NotImplementedError

    def is_surrounded(self) -> bool:  
        # Check if both ends of the sequence are closed by an opponent's stone.
        return (min(self.distance_to_edge) > 0
                and self.grid[self._previous_idx(1)] == (self.color * -1)
                and self.grid[self._next_idx(1)] == (self.color * -1))

    def is_captured(self) -> bool:
        return self.length == 2 and self.is_surrounded()
    
    def is_a_grouped_free_three(self) -> bool:
        # Check if the sequence is grouped free-three: e.g. [ . X X X . . ]
        # Check the length and if the immediate borders are free.
        if (self.length == 3 
            and min(self.distance_to_edge) > 0 and max(self.distance_to_edge) > 1
            and self.grid[self._previous_idx(1)] == 0
            and self.grid[self._next_idx(1)] == 0):
            # Check if there is a second available space after one of the immediate borders.
            if self.distance_to_edge[0] > 1:
                if self.grid[self._previous_idx(2)] == 0:
                    return True
            else:
                if self.grid[self._next_idx(2)] == 0:
                    return True
        return False

    def is_a_bridge(self) -> bool:
        # Check if the sequence is a 'bridge': e.g. [ . X . X X . ]
        # Check the length and if the immediate borders are free.
        if (self.length == 2 
            and min(self.distance_to_edge) > 0 and max(self.distance_to_edge) > 2
            and self.grid[self._previous_idx(1)] == 0
            and self.grid[self._next_idx(1)] == 0):
            # Check if there is an friendly stone beyond of the immediate borders.
            if self.distance_to_edge[0] > 1:
                if (self.grid[self._previous_idx(2)] == self.color
                    and self.grid[self._previous_idx(3)] == 0):
                    return True
            else:
                if (self.grid[self._next_idx(2)] == self.color
                    and self.grid[self._next_idx(3)] == 0):
                    return True
        return False

    def is_a_free_three(self) -> bool:
        # Check if the sequence is either a grouped free-three or a bridge.
        return self.is_a_grouped_free_three() or self.is_a_bridge()

    def __eq__(self, o: object) -> bool:
        return self.length == o.length and self.start == o.start and type(self) == type(o)


class Row(StoneSequence):
    def __init__(self, length: int, position: Position, color: int, grid: np.ndarray) -> None:
        super().__init__(length, position, color, grid)
        self.end = self.start + Position(0, length - 1)
        self.max_height = self.grid.shape[0] - 1
        self.max_width = self.grid.shape[1] - 1
        self.distance_to_edge = (self.start[1], self.max_width - self.end[1])

    def _previous_idx(self, distance: int) -> Tuple[int, int]:
        return self.start[0], self.start[1] - distance
    
    def _next_idx(self, distance: int) -> Tuple[int, int]:
        return self.end[0], self.end[1] + distance

 
class Column(StoneSequence):
    def __init__(self, length: int, position: Position, color: int, grid: np.ndarray) -> None:
        super().__init__(length, position, color, grid)
        self.end = self.start + Position(length-1, 0)
        self.max_height = self.grid.shape[0] - 1
        self.max_widht = self.grid.shape[1] - 1
        self.distance_to_edge = self.start[0], self.max_height - self.end[0]

    def _previous_idx(self, distance: int) -> Tuple[int, int]:
        return self.start[0] - distance, self.start[1]
    
    def _next_idx(self, distance: int) -> Tuple[int, int]:
        return self.end[0] + distance, self.end[1]


class Diagonal(StoneSequence):
    def __init__(self, length: int, position: Position, color: int, grid: np.ndarray, left: bool) -> None:
        super().__init__(length, position, color, grid)
        self.left = left
        self.slope = 1 if left else -1
        self.end = self.start + Position(length -1 , self.slope * (length -1))
        self.max_height = self.grid.shape[0] - 1
        self.max_width = self.grid.shape[1] - 1
        self.distance_to_edge = self._get_distance_to_edge()

    def __repr__(self) -> str:
        return f"Diagonal: {self.start}, {self.end}, {self.left}, {self.length}"

    def _get_distance_to_edge(self) -> Tuple[int,int]:
        if self.left:
            return min(self.start[0], self.start[1]), min(self.max_height - self.end[0], self.max_width - self.end[1])
        else:
            return min(self.start[0], self.max_width - self.start[1]), min(self.max_height - self.end[0], self.end[1])

    def _previous_idx(self, distance: int) -> Tuple[int, int]:
        return self.start[0] - distance, self.start[1] - (self.slope * distance)
    
    def _next_idx(self, distance: int) -> Tuple[int, int]:
        return self.end[0] + distance, self.end[1] + (self.slope * distance)


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
                    seqs.append(StoneSequence(len_, Position(start_i, start_j), color, grid))
                    len_ = 0
            # Incorrect color.
            else:
                if len_ < 2:
                    start_j = j+1
                    len_ = 0
                else:
                    seqs.append(StoneSequence(len_, Position(start_i, start_j), color, grid))
                    len_ = 0
                    start_i, start_j = i, j+1
    return seqs

def measure_row(grid: np.ndarray, color: int) -> List[Row]:
    sequences = measure_sequence(grid, color)
    return [Row(seq.length, seq.start, seq.color, grid) for seq in sequences]

def measure_col(grid: np.ndarray, color: int) -> List[Column]:
    # Transpose the cols as rows to measure it
    cols_sequences = measure_sequence(grid.T, color)
    # Swap position to get it right
    cols = [Column(seq.length, seq.start.swap(), seq.color, grid) for seq in cols_sequences]
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

    l_diags = [Diagonal(seq.length, convert_to_pos(seq.start, i_max, left=True),  seq.color, grid, left=True) for seq in l_diags_as_row]
    r_diags = [Diagonal(seq.length, convert_to_pos(seq.start, i_max, left=False), seq.color, grid, left=False) for seq in r_diags_as_row]
    
    return l_diags + r_diags

def collect_sequences(grid: np.ndarray, color: int) -> List[StoneSequence]:
    sequences = []
    sequences.extend(measure_row(grid, color))
    sequences.extend(measure_col(grid, color))
    sequences.extend(measure_diag(grid, color))
    return sequences


# def stone_sum(grid: np.ndarray, color: int) -> int:
def stone_sum(grid: np.ndarray) -> int:
    # Returns the difference between the total of black and white stones. The bigger the better.
    return grid.sum() #* color

# def longest_line(grid: np.ndarray, color: int) -> int:
def longest_line(grid: np.ndarray) -> int:
    # Returns the difference between the longest black and white lines of stones. The bigger the better. 
    black_max = max([measure_row(grid, BLACK), measure_col(grid, BLACK), measure_diag(grid, BLACK)])
    white_max = max([measure_row(grid, WHITE), measure_col(grid, WHITE), measure_diag(grid, WHITE)])
    # if color == BLACK:
    return black_max - white_max
    # return white_max - black_max