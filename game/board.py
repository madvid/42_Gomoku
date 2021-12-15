from __future__ import annotations
import numpy as np
import copy
from typing import Tuple, List

from game.metrics import *
from scipy import signal
from game.rules import iscapture_position

BLACK = 1
WHITE = -1
k_score = np.array([[1, 0, 1, 0, 1],
                    [0, 1, 1, 1, 0],
                    [1, 1, 1, 1, 1],
                    [0, 1, 1, 1, 0],
                    [1, 0, 1, 0, 1]])
class Node():
    # Global attributes of all nodes. Generated once before building the tree.
    metric: dict = {} # A dict containing the scoring metrics for black and white
        
    def __init__(self, parent: Node, grid: np.ndarray, color: int, max_seq_length: int = 0, current_pos:Tuple[int, int] = None) -> None:
        self.parent = parent
        self.grid = grid
        self.current_pos = current_pos
        self.color = color # Color of the player generating this move.
        self.nb_free_three = None # Attribute updated after the creation of the instance.
        self.stone_seq = {BLACK:[], WHITE:[]} # FIXME: REMOVE ME
        self.max_seq_length = max_seq_length
        self.update_score()

    def is_terminal(self):
        return self.max_seq_length >= 5

    def update(self, pos: Tuple[int,int], color: int) -> Node:
        tmp_grid = np.copy(self.grid)
        tmp_grid[pos] = color
        max_seq_length = collect_sequences(tmp_grid, color)
        return Node(self, tmp_grid, color * -1, max_seq_length, pos)

    def update_score(self):
        if self.parent is None or self.current_pos is None:
            self.scoreboard = np.zeros((19, 19))
            return
        else:
            self.scoreboard = self.parent.scoreboard
        yx = np.array((self.current_pos))
        print("yx :", yx)
        print(k_score)
        extend_grid = np.pad(self.grid, (4,4), 'constant', constant_values = 0)
        print("extend_grid:\n", extend_grid)
        extend_scoreboard = np.pad(self.scoreboard, (2,2), 'constant', constant_values = 0)
        
        
        #extend_scoreboard[yx[0] - 2 : yx[0] + 5, yx[1] : yx[1] + 5] = signal.convolve2d(extend_grid[yx[0] - 2: yx[0] + 7, yx[1] - 2: yx[1] + 7], k_score, "valid")
        tmp = signal.convolve2d(extend_grid[yx[0] - 2: yx[0] + 7, yx[1] - 2: yx[1] + 7], k_score, "full")
        print(tmp)
        self.scoreboard = extend_scoreboard[2:-2, 2:-2]
        print("score board:\n", self.scoreboard)

    # def remove_sequences(self, grid: np.ndarray, sequences: List[StoneSequence]) -> np.ndarray:
    #     def remove_row(grid: np.ndarray, row: Row):
    #         for i in range(row.length):
    #             grid[row.start[0], row.start[1] + i] = 0
    #         return grid
        
    #     def remove_col(grid: np.ndarray, col: Column):
    #         for i in range(col.length):
    #             grid[col.start[0] + i, col.start[1]] = 0
    #         return grid

    #     def remove_diag(grid: np.ndarray, diag: Diagonal):
    #         for i in range(diag.length):
    #             if diag.left:
    #                 grid[diag.start[0] + i, diag.start[1] + i] = 0
    #             else:
    #                 grid[diag.start[0] + i, diag.start[1] - i] = 0
    #         return grid
        
    #     rm_funcs = {
    #         Row: remove_row,
    #         Column: remove_col,
    #         Diagonal: remove_diag
    #     }
    #     for seq in sequences:
    #         tmp_grid = copy.deepcopy(grid)
    #         tmp_grid = rm_funcs[type(seq)](tmp_grid, seq)
    #         grid = tmp_grid
    #     return grid


    def generate_next_moves(self, color: int) -> List[Node]:
        possibles_moves_idx = np.argwhere(self.grid == 0)
        possibles_moves = [self.update((x,y), color) for x,y in possibles_moves_idx]
        for m in possibles_moves:
            

            # m.stone_seq[BLACK] = collect_sequences(m.grid, BLACK)
            # m.stone_seq[WHITE] = collect_sequences(m.grid, WHITE)
            # stone_seq: List[StoneSequence] = collect_sequences(m.grid, BLACK) + collect_sequences(m.grid, WHITE)
            # Captured stones
            iscapture_position(m.grid, m.last_coord, m.color)
            # captured_black_stones = filter(lambda x: x.length == 2 and x.is_surrounded(), m.stone_seq[BLACK])
            # captured_white_stones = filter(lambda x: x.length == 2 and x.is_surrounded(), m.stone_seq[WHITE])
            # captured_stones = filter(lambda x: x.length == 2 and x.is_surrounded(), m.stone_seq[BLACK] + m.stone_seq[WHITE])
            # print(f"captured = {captured_stones[0].grid}")
            # m.grid = self.remove_sequences(m.grid, captured_black_stones)
            # m.grid = self.remove_sequences(m.grid, captured_white_stones)
            # m.stone_seq[BLACK] = [s for s in m.stone_seq[BLACK] if not (s.length == 2 and s.is_surrounded())]
            # m.stone_seq[WHITE] = [s for s in m.stone_seq[WHITE] if not (s.length == 2 and s.is_surrounded())]

            # # Double free-three
            # cleared_stone_seq: List[StoneSequence] = collect_sequences(m.grid, BLACK) + collect_sequences(m.grid, WHITE)
            # m.nb_free_three = len(list(filter(lambda x: x.is_a_free_three(), cleared_stone_seq)))
            # # FIXME: double-three share a common stone!

            # print(m.parent)
            # print(m.nb_free_three)
            # print(self.parent.nb_free_three)
         
            # if m.nb_free_three == self.parent.nb_free_three + 2:
            #     possibles_moves.remove(m)

            # FIXME: double three are allowed if resulting from a capture!
        return possibles_moves

    def score(self, color: int) -> int:
        return Node.metric[color](self)


    # def score(self, color: int) -> int:
    #     return Node.metric[color](self.grid)



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


def sum_longest(node: Node) -> int:
    return longest_line(node)**2 + stone_sum(node.grid)

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