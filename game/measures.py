import numpy as np
from typing import List, Tuple
from metrics import *
from board import *
from minimax import * 

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

# def update_sequences(grid: np.ndarray, color: int, sequences: List[StoneSequence], pos: Position) -> List[StoneSequence]:
#     for s in sequences:
#         if s.contains(pos):


def stone_sum(grid: np.ndarray) -> int:
    # Returns the difference between the total of black and white stones. The bigger the better.
    return grid.sum()

def longest_line(node: Node) -> int:
    # Returns the difference between the longest black and white lines of stones. The bigger the better. 
    black_max = max(node.stone_seq[BLACK], key=lambda x: x.length) if node.stone_seq[BLACK] != [] else 0
    white_max = max(node.stone_seq[WHITE], key=lambda x: x.length) if node.stone_seq[WHITE] != [] else 0
    return black_max - white_max

# def longest_line(grid: np.ndarray) -> int:
#     # Returns the difference between the longest black and white lines of stones. The bigger the better. 
#     black_seq = [x.length for x in collect_sequences(grid, BLACK)]
#     white_seq = [x.length for x in collect_sequences(grid, WHITE)]
#     black_max = max(black_seq) if black_seq != [] else 0
#     white_max = max(white_seq) if white_seq != [] else 0
#     return black_max - white_max


def sum_longest(grid: np.ndarray) -> int:
    return longest_line(grid)**2 + stone_sum(grid)

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


def sum_dummy(grid: np.ndarray) -> int:
    return dummy_mask(grid) + longest_line(grid)

def sum_mask2(grid: np.ndarray) -> int:
    return mask2(grid) + longest_line(grid)

def sum_mask3(node: Node) -> int:
    return mask3(node.grid) + longest_line(node)

def sum_mask4(grid: np.ndarray) -> int:
    return mask4(grid) + longest_line(grid)


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

def sum_kern2(grid: np.ndarray) -> int:
    return kern2(grid) + longest_line(grid)

def sum_kern3(grid: np.ndarray) -> int:
    return kern3(grid) + longest_line(grid)

def sum_kern4(grid: np.ndarray) -> int:
    return kern4(grid) + longest_line(grid)