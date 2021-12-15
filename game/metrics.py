# =========================================================================== #
# ____________________  |Importation des lib/packages|   ____________________ #
# =========================================================================== #
from __future__ import annotations
from typing import List, Tuple, Callable
import numpy as np
from functools import partial
from numba import njit


# Typing related (type aliases, NewType, ...)
KernelOutput = Tuple[Tuple[int, int], Tuple[int, int]]

# =========================================================================== #
#                          | constants definition |                           #
# =========================================================================== #
BLACK = 1
WHITE = -1


kernels = np.array([[1, 1, 1, 1],
                    [1, 1, 1, 1],
                    [0, 1, 1, 1],
                    [0, 0, 1, 1],
                    [0, 0, 0, 1]])


# =========================================================================== #
#                           | Classes definition |                            #
# =========================================================================== #
class Position():
    def __init__(self, i: int, j: int) -> None:
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

    def is_surrounded(self, last_coord: Tuple[int, int]) -> bool:  
        # Check if both ends of the sequence are closed by an opponent's stone.
        return (min(self.distance_to_edge) > 0
                and self.grid[self._previous_idx(1)] == (self.color * -1)
                and self.grid[self._next_idx(1)] == (self.color * -1)
                and (last_coord in (self._next_idx(1), self._previous_idx(1))))

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
    LEFT = True
    def __init__(self, length: int, position: Position, color: int, grid: np.ndarray, left: bool=None) -> None:
        super().__init__(length, position, color, grid)
        if left is None:
            self.left = Diagonal.LEFT
        else:
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


# =========================================================================== #
#                          | Functions definition |                           #
# =========================================================================== #
@njit(parallel=True, fastmath=True)
def _DEPRECATED_measure_sequence_numba(grid: np.ndarray, color: int) -> List[int]:
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
                    seqs.append((len_, start_i, start_j))
                    # seqs.append(StoneSequence(len_, Position(start_i, start_j), color, grid))
                    len_ = 0
            # Incorrect color.
            else:
                if len_ < 2:
                    start_j = j+1
                    len_ = 0
                else:
                    seqs.append((len_, start_i, start_j))
                    # seqs.append(StoneSequence(len_, Position(start_i, start_j), color, grid))
                    len_ = 0
                    start_i, start_j = i, j+1
    return seqs


def _DEPRECATED_measure_sequence(grid: list, color: int) -> list:
    numba_seqs = measure_sequence_numba(grid, color)
    return [(len_, (start_i, start_j), color, grid) for len_, start_i, start_j in numba_seqs]

# def measure_sequence(grid: np.ndarray, color: int) -> List[StoneSequence]:
def _DEPRECATED_measure_sequence_(grid: np.ndarray, color: int) -> list:
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
                    # seqs.append((len_, (start_i, start_j), color, grid))
                    seqs.append(StoneSequence(len_, Position(start_i, start_j), color, grid))
                    len_ = 0
            # Incorrect color.
            else:
                if len_ < 2:
                    start_j = j+1
                    len_ = 0
                else:
                    # seqs.append((len_, (start_i, start_j), color, grid))
                    seqs.append(StoneSequence(len_, Position(start_i, start_j), color, grid))
                    len_ = 0
                    start_i, start_j = i, j+1
    return seqs


def _DEPRECATED_measure_row(grid: np.ndarray, color: int) -> List[Row]:
    sequences = measure_sequence(grid, color)
    return [Row(len_, Position(pos[0], pos[1]), color, grid) for len_, pos, color, grid in sequences]
    # return [Row(seq.length, seq.start, seq.color, grid) for seq in sequences]


def _DEPRECATED_measure_col(grid: np.ndarray, color: int) -> List[Column]:
    # Transpose the cols as rows to measure it
    cols_sequences = measure_sequence(grid.T, color)
    # Swap position to get it right
    return [Column(len_, Position(pos[0], pos[1]).swap(), color, grid) for len_, pos, color, grid in cols_sequences]
    # cols = [Column(seq.length, seq.start.swap(), seq.color, grid) for seq in cols_sequences]
    # return cols


def _DEPRECATED_measure_diag(grid: np.ndarray, color: int) -> List[Diagonal]:
    i_max = grid.shape[0] - 1
    l_diags_lst = [np.diag(grid, k=n) for n in range(-grid.shape[0]+1, grid.shape[1])]
    r_diags_lst = [np.diag(np.fliplr(grid), k=n) for n in range(-grid.shape[0]+1, grid.shape[1])]
    
    l_diags_as_row = measure_sequence_(l_diags_lst, color)
    r_diags_as_row = measure_sequence_(r_diags_lst, color)

    # l_diags = [Diagonal(len_, convert_to_pos(Position(pos[0], pos[1]), i_max, left=True), color, grid, left=True) for len_, pos, color, grid in l_diags_as_row]
    l_diags = [Diagonal(seq.length, convert_to_pos(seq.start, i_max, left=True),  seq.color, grid, left=True) for seq in l_diags_as_row]
    # r_diags = [Diagonal(len_, convert_to_pos(Position(pos[0], pos[1]), i_max, left=True), color, grid, left=False) for len_, pos, color, grid in r_diags_as_row]
    r_diags = [Diagonal(seq.length, convert_to_pos(seq.start, i_max, left=False), seq.color, grid, left=False) for seq in r_diags_as_row]

    return l_diags + r_diags


def _DEPRECATED_convert_to_pos(d_pos: Position, i_max: int, left: bool = True) -> Position:
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


def get_kern_row_idx(pos: Tuple[int,int]) -> KernelOutput:
    return [pos[0]] * 5, range(pos[1], pos[1] + 5)


def get_kern_col_idx(pos: Tuple[int,int]) -> KernelOutput:
    return range(pos[0], pos[0] + 5), [pos[1]] * 5


def get_kern_diag_idx(pos: Tuple[int,int]) -> KernelOutput:
    return range(pos[0], pos[0] + 5), range(pos[1], pos[1] + 5)


# @njit(parallel=True, fastmath=True)
def measure_sequence(grid: np.ndarray, color: int, get_kernel_idx: Callable[[Tuple[int, int]], KernelOutput], seq_type: StoneSequence) -> List[StoneSequence]: # FIXME:  typage 
    """[summary]

    Args:
        grid (np.ndarray): [description]
        color (int): [description]

    Returns:
        List[Row]: [description]
    """
    extend_grid = np.pad(grid, (0, 5), "constant", constant_values=(0, 0))
    stack = np.argwhere(extend_grid == color)
    res = []
    i = 0
    while i < stack.shape[0]:
        tmp = np.dot(extend_grid[get_kernel_idx(stack[i])], kernels)
        # tmp = (tmp / np.arange(2, 6)).astype('int8').sum(axis=1) + 1
        tmp = (tmp / np.arange(2, 6)).astype('int8').sum() + 1
        if tmp > 1:
            res.append(seq_type(length=tmp, position=Position(stack[i][0],stack[i][1]), grid=grid, color=color)) # FIXME: change POSITION class and methods
            i += res[-1].length - 1
        else:
            i += 1
    
    return res

  
def measure_row(grid: np.ndarray, color: int) -> List[Row]:
    return measure_sequence(grid, color, get_kern_row_idx, Row)


def measure_col(grid: np.ndarray, color: int) -> List[Column]:
    return measure_sequence(grid, color, get_kern_col_idx, Column)


def measure_diag(grid: np.ndarray, color: int, left: bool) -> List[Diagonal]:
    if left:
        Diagonal.LEFT = True
        return measure_sequence(grid, color, get_kern_diag_idx, Diagonal)
    else:
        Diagonal.LEFT = False
        return measure_sequence(grid, color, get_kern_diag_idx, Diagonal)


def collect_sequences(grid: np.ndarray, color: int) -> List[StoneSequence]:
    sequences = []
    sequences.extend(measure_row(grid, color))
    sequences.extend(measure_col(grid, color))
    sequences.extend(measure_diag(grid, color, True))
    sequences.extend(measure_diag(np.fliplr(grid), color, False))
    return sequences

# def update_sequences(grid: np.ndarray, color: int, sequences: List[StoneSequence], pos: Position) -> List[StoneSequence]:
#     for s in sequences:
#         if s.contains(pos):


