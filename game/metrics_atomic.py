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



# =========================================================================== #
#                          | Functions definition |                           #
# =========================================================================== #

def get_kern_row_idx(pos: Tuple[int,int], direction: int = 1, length: int = 5) -> KernelOutput:
    return pos[0] * np.ones(length, dtype = 'int8'), np.arange(pos[1], pos[1] + direction * length, direction)


def get_kern_col_idx(pos: Tuple[int,int], direction: int = 1, length: int = 5) -> KernelOutput:
    return np.arange(pos[0], pos[0] + direction * length, direction), [pos[1]] * np.ones(length, dtype = 'int8')


def get_kern_diag_idx(pos: Tuple[int,int], slope:Tuple(int, int) = 1, length: int = 5) -> KernelOutput:
    return np.arange(pos[0], pos[0] + slope[0] * length, slope[0]), np.arange(pos[1], pos[1] + slope[1] * length, slope[1])


# @njit(parallel=True, fastmath=True)
def measure_sequence(grid: np.ndarray, color: int, position: Tuple[int, int], get_kernel_idx: Callable[[Tuple[int, int]], KernelOutput]) -> int: # FIXME:  typage 
    """[summary]

    Args:
        grid (np.ndarray): [description]
        color (int): [description]

    Returns:
        List[Row]: [description]
    """
    extend_grid = np.pad(grid, (0, 5), "constant", constant_values=(0, 0))
    stack = np.argwhere(extend_grid == color)
    res = [1]
    i = 0
    while i < stack.shape[0]:
        tmp = np.dot(extend_grid[get_kernel_idx(stack[i])], kernels)
        tmp = (tmp / np.arange(2, 6)).astype('int8').sum() + 1
        if tmp > 1:
            res.append(tmp)
            i += res[-1] - 1
        else:
            i += 1
    return max(res)

def measure_row(grid: np.ndarray, position: Tuple[int, int], color: int) -> int:
    return measure_sequence(grid, position, color, get_kern_row_idx)

def measure_col(grid: np.ndarray, position: Tuple[int, int], color: int) -> int:
    return measure_sequence(grid, position, color, get_kern_col_idx)

def measure_diag(grid: np.ndarray, position: Tuple[int, int], color: int, left: bool) -> int:
    if left:
        return measure_sequence(grid, position, color, get_kern_diag_idx)
    else:
        return measure_sequence(np.fliplr(grid), position, color, get_kern_diag_idx)

def collect_sequences(grid: np.ndarray, position: Tuple[int,int], color: int) -> int:
    sequences = []
    sequences.append(measure_row(grid, position, color))
    sequences.append(measure_col(grid, position, color))
    sequences.append(measure_diag(grid, position, color, True))
    sequences.append(measure_diag(np.fliplr(grid), position, color, False))
    return max(sequences)


