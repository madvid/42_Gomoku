from __future__ import annotations
import numpy as np
from scipy import signal
import copy
from typing import Tuple, List

from game.metrics import Row, Column, Diagonal
from game.metrics import collect_sequences

# =========================================================================== #
# ___________________________    |CONSTANTES|    ____________________________ #
# =========================================================================== #

BLACK = 1
WHITE = -1


# =========================================================================== #
# ___________________________    |FUNCTIONS|     ____________________________ #
# =========================================================================== #

def stone_sum(grid: np.ndarray) -> int:
    # Returns the difference between the total of black and white stones. The bigger the better.
    return grid.sum()

def longest_line(node: Node) -> int:
    # Returns the difference between the longest black and white lines of stones. The bigger the better. 
    black_max = max([n.length for n in node.stone_seq[BLACK]]) if node.stone_seq[BLACK] != [] else 0
    white_max = max([n.length for n in node.stone_seq[WHITE]]) if node.stone_seq[WHITE] != [] else 0
    return black_max - white_max

# def longest_line(grid: np.ndarray) -> int:
#     # Returns the difference between the longest black and white lines of stones. The bigger the better. 
#     black_seq = [x.length for x in collect_sequences(grid, BLACK)]
#     white_seq = [x.length for x in collect_sequences(grid, WHITE)]
#     black_max = max(black_seq) if black_seq != [] else 0
#     white_max = max(white_seq) if white_seq != [] else 0
#     return black_max - white_max


def sum_longest(grid: np.ndarray) -> int:
    return longest_line(node)**2 + stone_sum(grid)

def dummy_mask(grid: np.ndarray) -> int:
    msk = np.array([
        [1, 1, 1, 1, 1, 1],
        [1, 2, 2, 2, 2, 1],
        [1, 2, 3, 3, 2, 1],
        [1, 2, 3, 3, 2, 1],
        [1, 2, 2, 2, 2, 1],
        [1, 1, 1, 1, 1, 1],
    ])
    return np.sum(grid * msk)


def mask2(grid: np.ndarray) -> int:
    kernel = np.array(
    [
        [1, 0, 1, 0, 1],
        [0, 1, 1, 1, 0],
        [1, 1, 1, 1, 1],
        [0, 1, 1, 1, 0],
        [1, 0, 1, 0, 1],
    ]
)
    mask = signal.convolve2d(np.ones(grid.shape), kernel / kernel.sum(), mode='same')
    return np.sum(mask * grid)


def mask3(grid: np.ndarray) -> int:
    kernel = np.array(
    [
        [1, 0, 0, 1, 0, 0, 1],
        [0, 1, 0, 1, 0, 1, 0],
        [0, 0, 1, 1, 1, 0, 0],
        [1, 1, 1, 1, 1, 1, 1],
        [0, 0, 1, 1, 1, 0, 0],
        [0, 1, 0, 1, 0, 1, 0],
        [1, 0, 0, 1, 0, 0, 1],
    ]
)
    mask = signal.convolve2d(np.ones(grid.shape), kernel / kernel.sum(), mode='same')
    return np.sum(mask * grid)
    
# def mask3(grid: np.ndarray) -> int:
#     kernel = np.array(
#     [
#         [1, 0, 0, 1, 0, 0, 1],
#         [0, 1, 0, 1, 0, 1, 0],
#         [0, 0, 1, 1, 1, 0, 0],
#         [1, 1, 1, 1, 1, 1, 1],
#         [0, 0, 1, 1, 1, 0, 0],
#         [0, 1, 0, 1, 0, 1, 0],
#         [1, 0, 0, 1, 0, 0, 1],
#     ]
# )
#     mask = signal.convolve2d(np.ones(grid.shape), kernel / kernel.sum(), mode='same')
#     return np.sum(mask * grid)


def mask4(grid: np.ndarray) -> int:
    kernel = np.array(
    [
        [1, 0, 0, 0, 1, 0, 0, 0, 1],
        [0, 1, 0, 0, 1, 0, 0, 1, 0],
        [0, 0, 1, 0, 1, 0, 1, 0, 0],
        [0, 0, 0, 1, 1, 1, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 1, 1, 1, 0, 0, 0],
        [0, 0, 1, 0, 1, 0, 1, 0, 0],
        [0, 1, 0, 0, 1, 0, 0, 1, 0],
        [1, 0, 0, 0, 1, 0, 0, 0, 1],
    ]
)
    mask = signal.convolve2d(np.ones(grid.shape), kernel / kernel.sum(), mode='same')
    return np.sum(mask * grid)


def sum_dummy(node: Node) -> int:
    return dummy_mask(node.grid) + longest_line(node)

def sum_mask2(node: Node) -> int:
    return mask2(node.grid) + longest_line(node)

def sum_mask3(node: Node) -> int:
    return mask3(node.grid) + longest_line(node)

def sum_mask4(node: Node) -> int:
    return mask4(node.grid) + longest_line(node)


def kern2(grid: np.ndarray) -> int:
    kernel = np.array(
    [
        [1, 0, 1, 0, 1],
        [0, 1, 1, 1, 0],
        [1, 1, 1, 1, 1],
        [0, 1, 1, 1, 0],
        [1, 0, 1, 0, 1],
    ]
)
    return np.sum(signal.convolve2d(grid, kernel / kernel.sum(), mode='same'))


def kern3(grid: np.ndarray) -> int:
    kernel = np.array(
    [
        [1, 0, 0, 1, 0, 0, 1],
        [0, 1, 0, 1, 0, 1, 0],
        [0, 0, 1, 1, 1, 0, 0],
        [1, 1, 1, 1, 1, 1, 1],
        [0, 0, 1, 1, 1, 0, 0],
        [0, 1, 0, 1, 0, 1, 0],
        [1, 0, 0, 1, 0, 0, 1],
    ]
)
    return np.sum(signal.convolve2d(grid, kernel / kernel.sum(), mode='same'))


def kern4(grid: np.ndarray) -> int:
    kernel = np.array(
    [
        [1, 0, 0, 0, 1, 0, 0, 0, 1],
        [0, 1, 0, 0, 1, 0, 0, 1, 0],
        [0, 0, 1, 0, 1, 0, 1, 0, 0],
        [0, 0, 0, 1, 1, 1, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 1, 1, 1, 0, 0, 0],
        [0, 0, 1, 0, 1, 0, 1, 0, 0],
        [0, 1, 0, 0, 1, 0, 0, 1, 0],
        [1, 0, 0, 0, 1, 0, 0, 0, 1],
    ]
)
    return np.sum(signal.convolve2d(grid, kernel / kernel.sum(), mode='same'))

def sum_kern2(node: Node) -> int:
    return kern2(node.grid) + longest_line(node)

def sum_kern3(node: Node) -> int:
    return kern3(node.grid) + longest_line(node)

def sum_kern4(node: Node) -> int:
    return kern4(node.grid) + longest_line(node)
