from __future__ import annotations
import numpy as np
import copy
from typing import Tuple, List
from heapq import *

from game.metrics import *
from scipy.signal import convolve2d
from game.rules import iscapture_position, remove_opponent_pair

BLACK = 1
WHITE = -1
k_croix = np.array([[1, 0, 1, 0, 1],
                    [0, 1, 1, 1, 0],
                    [1, 1, 1, 1, 1],
                    [0, 1, 1, 1, 0],
                    [1, 0, 1, 0, 1]])
class Node():
    # Global attributes of all nodes. Generated once before building the tree.
    metric: dict = {BLACK: max, WHITE: min} # A dict containing the scoring metrics for black and white
        
    def __init__(self, parent: Node, grid: np.ndarray, color: int, max_seq_length: int = 0, pos:Tuple[int, int] = None) -> None:
        self.parent = parent
        self.grid = grid # Should be a 27 x 27 boardgame (i.e a padded one)
        self.current_pos = pos # Should be the padded current position (true position on real board + (4,4))
        self.color = color # Color of the player generating this move.
        self.nb_free_three = None # Attribute updated after the creation of the instance.
        self.stone_seq = {BLACK:[], WHITE:[]} # FIXME: REMOVE ME
        self.max_seq_length = max_seq_length
        self.scoreboard = self.init_scoreboard()
        self.scoreboard[self.color][pos[0] : pos[0] + 5, pos[1] :pos[1] + 5] = self.update_score([k_croix], [1]) # update scoreboard with each kernel ponderated by the corresponding coef

    def is_terminal(self):
        return self.max_seq_length[BLACK] >= 5 or self.max_seq_length[WHITE] >= 5

    def update(self, pos: Tuple[int,int], color: int) -> Node:
        tmp_grid = np.copy(self.grid)
        tmp_grid[pos] = color
        black_max_seq_length = collect_sequences(tmp_grid, BLACK)
        white_max_seq_length = collect_sequences(tmp_grid, WHITE)
        return Node(self, tmp_grid, color * -1, {BLACK: black_max_seq_length, WHITE: white_max_seq_length}, pos)

    def init_scoreboard(self):
        if self.parent is None:
            return {WHITE: np.zeros((27,27)), BLACK: np.zeros((27,27))}
        else:
            return copy.deepcopy(self.parent.scoreboard)

    def update_score(self, k_list, c_list):
        score = np.zeros((5, 5))
        for c, k in zip(c_list, k_list):
            score += self.apply_kern(c * k)
        return score

    def apply_kern(self, k_score: np.array):
        if self.current_pos is None:
            return np.zeros((5, 5))
        tmp = self.grid # it could the opposite color, who knows ...
        yx = np.array((self.current_pos))
        return  convolve2d(tmp[yx[0] - 4: yx[0] + 5, yx[1] - 4: yx[1] + 5], k_score, "valid")

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

    def _DEPRECATED_generate_next_moves(self, color: int) -> List[Node]:
        # possibles_moves_idx = np.argwhere(self.grid == 0)
        # possibles_moves = [self.update((x,y), color) for x,y in possibles_moves_idx]

        # kernel = np.array([
        #     [1, 1, 1],
        #     [1, 0, 1],
        #     [1, 1, 1]
        # ])

        kernel = np.array([
            [1, 0, 1, 0, 1],
            [0, 1, 1, 1, 0],
            [1, 1, 1, 1, 1],
            [0, 1, 1, 1, 0],
            [1, 0, 1, 0, 1]
        ])
        mask = (convolve2d(self.grid, kernel / kernel.sum(), mode='same') > 1) & (self.grid == 0)
        possibles_moves_idx = np.argwhere(mask != 0)
        possibles_moves = [self.update((x,y), color) for x,y in possibles_moves_idx]
        # print(possibles_moves)
        for m in possibles_moves:
            
            # m.stone_seq[BLACK] = collect_sequences(m.grid, BLACK)
            # m.stone_seq[WHITE] = collect_sequences(m.grid, WHITE)
            # stone_seq: List[StoneSequence] = collect_sequences(m.grid, BLACK) + collect_sequences(m.grid, WHITE)
            # Captured stones
            iscapture_position(m.grid, m.current_pos, m.color)
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

    def generate_next_moves(self, color: int) -> List[Node]:
        # possibles_moves_idx = np.argwhere(self.grid == 0)
        # possibles_moves = [self.update((x,y), color) for x,y in possibles_moves_idx]
        
        mask = self.grid[4:-4, 4:-4] == 0
        possibles_moves_idx = np.argwhere(mask != 0)
        # We add +4 to the following x and y due to the fact the grid is padded 
        possibles_moves = [(-abs(self.scoreboard[self.color][4:-4, 4:-4][x,y]), self.update((x + 4,y + 4), color)) for x,y in possibles_moves_idx]
        
        for _, m in possibles_moves:
            # Captured stones
            pos_to_rm = iscapture_position(m.grid, m.current_pos, m.color)
            remove_opponent_pair(m.grid, pos_to_rm)
           
            # # Double free-three

        heapify(possibles_moves)
        return possibles_moves

    def score(self, color: int) -> int:
        return self.metric[color](self.scoreboard[color])

    # def score(self, color: int) -> int:
    #     return Node.metric[color](self.grid)
    
    def __lt__(self, other):
        return abs(self.scoreboard[self.].sum()) * self.color < abs(other.scoreboard[self.].sum()) * other.color


    def __gt__(self, other):
        return abs(self.scoreboard.sum()) * self.color > abs(other.scoreboard.sum()) * other.color


def stone_sum(grid: np.ndarray) -> int:
    # Returns the difference between the total of black and white stones. The bigger the better.
    return grid.sum()

def longest_line(node: Node) -> int:
    # Returns the difference between the longest black and white lines of stones. The bigger the better. 
    # black_max = max([n.length for n in node.stone_seq[BLACK]]) if node.stone_seq[BLACK] != [] else 0
    # white_max = max([n.length for n in node.stone_seq[WHITE]]) if node.stone_seq[WHITE] != [] else 0
    print(f"longuest line: {node.max_seq_length[BLACK] - node.max_seq_length[WHITE]}")
    return node.max_seq_length[BLACK] - node.max_seq_length[WHITE]

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
    mask = convolve2d(np.ones(grid.shape), kernel / kernel.sum(), mode='same')
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
    mask = convolve2d(np.ones(grid.shape), kernel / kernel.sum(), mode='same')
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
#     mask = convolve2d(np.ones(grid.shape), kernel / kernel.sum(), mode='same')
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
    mask = convolve2d(np.ones(grid.shape), kernel / kernel.sum(), mode='same')
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
    return np.sum(convolve2d(grid, kernel / kernel.sum(), mode='same'))


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
    return np.sum(convolve2d(grid, kernel / kernel.sum(), mode='same'))


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
    return np.sum(convolve2d(grid, kernel / kernel.sum(), mode='same'))

def sum_kern2(node: Node) -> int:
    return kern2(node.grid) + longest_line(node)

def sum_kern3(node: Node) -> int:
    return kern3(node.grid) + longest_line(node)

def sum_kern4(node: Node) -> int:
    return kern4(node.grid) + longest_line(node)