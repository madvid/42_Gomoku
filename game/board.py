from __future__ import annotations
import numpy as np
import copy
from typing import Tuple, List
from heapq import *

from game.metrics import *
from scipy.signal import convolve2d
from game.rules import iscapture_position, remove_opponent_pair
np.set_printoptions(linewidth = 200)

BLACK = 1
WHITE = -1
k_croix = np.array([[1, 0, 1, 0, 1],
                    [0, 1, 1, 1, 0],
                    [1, 1, 1, 1, 1],
                    [0, 1, 1, 1, 0],
                    [1, 0, 1, 0, 1]])

k_little_square = np.array([[0, 0, 0, 0, 0],
                            [0, 1, 1, 1, 0],
                            [0, 1, 1, 1, 0],
                            [0, 1, 1, 1, 0],
                            [0, 0, 0, 0, 0]])

k_nxt_opponent = np.array([[0,  0,  0,  0, 0],
                           [0, -1, -1, -1, 0],
                           [0, -1,  0, -1, 0],
                           [0, -1, -1, -1, 0],
                           [0,  0,  0,  0, 0]])

k_5_stones = np.array([1, 1, 1, 1, 1])

class Node():
    # Global attributes of all nodes. Generated once before building the tree.
    metric: dict = {BLACK: np.max, WHITE: np.min} # A dict containing the scoring metrics for black and white
        
    def __init__(self, parent: Node, grid: np.ndarray, color: int, pos:Tuple[int, int] = None) -> None:
        self.parent = parent
        self.grid = grid # Should be a 27 x 27 boardgame (i.e a padded one)
        self.current_pos = pos # Should be the padded current position (true position on real board + (4,4))
        self.color = color # Color of the player generating this move.
        self.nb_free_three = None # Attribute updated after the creation of the instance.
        self.isterminal = None
        self.stone_seq = {BLACK:[], WHITE:[]} # FIXME: REMOVE ME
        self.scoreboard = self.init_scoreboard()

        if not pos is None:
            self.scoreboard[self.color][pos[0] - 2: pos[0] + 3, pos[1] - 2:pos[1] + 3] = self.update_score([self.color * k_croix], [1]) # update scoreboard with each kernel ponderated by the corresponding coef
            # self.scoreboard[self.color][pos[0] - 2: pos[0] + 3, pos[1] - 2:pos[1] + 3] = self.update_score([self.color * k_nxt_opponent], [1]) # update scoreboard with each kernel ponderated by the corresponding coef

            ########################################################################
            # FIXME: should the code below be put in a dedicated func?
            pos_to_rm = iscapture_position(self.grid, self.current_pos, self.color)
            remove_opponent_pair(self.grid, pos_to_rm)
            ########################################################################


    def is_terminal(self) -> bool:
        """Evaluates if the node is a terminal one, meaning the conditions of victory are met.
        Victory of a player is when:
            * the player has a sequence of 5 stones,
            * None of the stones among the sequence of 5 can be captured.

        Returns:
            bool: True -> game finished
                  Fasle -> game not finished yet
        """
        r_conv = []
        # Check 5 stones along column
        r_conv.append(np.dot(self.grid[get_kern_col_idx(self.current_pos, -1, 5)], self.color * k_5_stones))
        r_conv.append(np.dot(self.grid[get_kern_col_idx(self.current_pos, 1, 5)], self.color * k_5_stones))
        # Check 5 stones along row
        r_conv.append(np.dot(self.grid[get_kern_row_idx(self.current_pos, -1, 5)], self.color * k_5_stones))
        r_conv.append(np.dot(self.grid[get_kern_row_idx(self.current_pos, 1, 5)], self.color * k_5_stones))
        # Check 5 stones along diagonals
        r_conv.append(np.dot(self.grid[get_kern_diag_idx(self.current_pos, (-1, -1), 5)], self.color * k_5_stones))
        r_conv.append(np.dot(self.grid[get_kern_diag_idx(self.current_pos, (-1, 1), 5)], self.color * k_5_stones))
        r_conv.append(np.dot(self.grid[get_kern_diag_idx(self.current_pos, (1, -1), 5)], self.color * k_5_stones))
        r_conv.append(np.dot(self.grid[get_kern_diag_idx(self.current_pos, (1, 1), 5)], self.color * k_5_stones))
        if any([r == 5 for r in r_conv]):
            return True
        return False

    def update(self, pos: Tuple[int,int], adv_color: int) -> Node:
        
        nw_grid = np.copy(self.grid)
        nw_grid[pos] = adv_color
        
        return Node(parent = self, grid = nw_grid, color = adv_color, pos = pos)

    def init_scoreboard(self):
        if self.parent is None:
            return {WHITE: convolve2d(self.grid, k_croix, "same"), BLACK: convolve2d(self.grid, k_croix, "same")}
        else:
            return copy.deepcopy(self.parent.scoreboard)

    def update_score(self, k_list, c_list):
        score = np.zeros((5, 5))
        
        for c, k in zip(c_list, k_list):
            score += self.apply_kern(c * k)
        self.isterminal = self.is_terminal()
        if self.isterminal:
            score[2][2] += self.color * 1000 
        return score
    
    # def update_score(self, k_list, c_list):
    #     score = np.zeros((5, 5))
    #     for c, k in zip(c_list, k_list):
    #         score += self.apply_kern(c * k)
    #     self.isterminal = self.is_terminal()
    #     if self.isterminal:
    #         score[2][2] += self.color * 1000 
    #     return score

    def score(self):
        #return collect_sequences(self.grid, self.color)
        return self.scoreboard[self.color][4:-4,4:-4].sum() #+ self.scoreboard[self.color][4:-4,4:-4].max()

    def apply_kern(self, k_score: np.array):
        if self.current_pos is None:
            return np.zeros((5, 5))
        tmp = self.grid # it could the opposite color, who knows ...
        yx = np.array((self.current_pos))
        #print(f"yx = {yx}")
        #print("sub view tmp[yx[0] - 4: yx[0] + 5, yx[1] - 4: yx[1] + 5]:\n",tmp[yx[0] - 4: yx[0] + 5, yx[1] - 4: yx[1] + 5])
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


    def generate_next_moves(self) -> List[Node]:
        # possibles_moves_idx = np.argwhere(self.grid == 0)
        # possibles_moves = [self.update((x,y), color) for x,y in possibles_moves_idx]

        kernel = np.array([
            [0, 0, 0, 0, 0],
            [0, 1, 1, 1, 0],
            [0, 1, 1, 1, 0],
            [0, 1, 1, 1, 0],
            [0, 0, 0, 0, 0]
        ])

        # kernel = np.array([
        #     [1, 1, 1],
        #     [1, 0, 1],
        #     [1, 1, 1]
        # ])
        mask = (convolve2d(np.absolute(self.grid[4:-4, 4:-4]), kernel, mode='same') >= 1) & (self.grid[4:-4, 4:-4] == 0)
        possibles_moves_idx = np.argwhere(mask != 0)
        # # sorted_mask = np.sort(mask, axis=None)#[np.unravel_index(np.argsort(mask, axis=None)[-1 * self.color:0:-1*self.color], (19,19))]
        # # print(sorted_mask)
        # # possibles_moves_idx = np.argwhere(sorted_mask != 0)

        # # print(possibles_moves_idx)

        # We add +4 to the following x and y due to the fact the grid is padded 
        #possibles_moves = [(-abs(self.scoreboard[self.color][4:-4, 4:-4][x,y]), self.update((x + 4,y + 4), -self.color)) for x,y in possibles_moves_idx]
        possibles_moves = (self.update((x + 4,y + 4), -self.color) for x,y in possibles_moves_idx)
        
        # heapify(possibles_moves)
        return possibles_moves

    # def score(self) -> int:
    #     return self.scoreboard[self.color][self.current_pos]
        # return self.metric[color](self.scoreboard[color]) + self.metric[-color](self.scoreboard[-color])

    # def score(self, color: int) -> int:
    #     return Node.metric[color](self.grid)
    
    def __lt__(self, other):
        return (abs(self.scoreboard[self.color].sum()) * self.color) < (abs(other.scoreboard[other.color].sum()) * other.color)


    def __gt__(self, other):
        return abs(self.scoreboard.sum()) * self.color > abs(other.scoreboard.sum()) * other.color


def stone_sum(grid: np.ndarray) -> int:
    # Returns the difference between the total of black and white stones. The bigger the better.
    return grid.sum()


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