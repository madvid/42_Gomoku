from __future__ import annotations
import numpy as np
from numpy import ndarray
from typing import Tuple, List

BLACK = 1
WHITE = -1

class Node():
    # Global attributes of all nodes. Generated once before building the tree.
    metric = None # A dict containing the scoring metrics for blakc and white
        
    def __init__(self, parent: Node, grid: ndarray, color: int = BLACK) -> None:
        self.parent = parent
        self.grid = grid
        self.color = color
    
    def update(self, pos: Tuple[int,int], color: int) -> Node:
        tmp_grid = np.deepcopy(self.grid)
        tmp_grid[pos] = color
        return Node(self, tmp_grid, color)

    def generate_next_moves(self) -> List[Node]:
        possibles_moves = np.argwhere(self.grid == 0)
        return [self.update(pos, self.color * -1) for pos in possibles_moves]

    def score(self):
        return Node.metric[self.color](self.grid, self.color)


def measure_row(grid: ndarray, color: int) -> int:
    max_len = 0
    for r in grid:
        len_ = 0
        for i in r:
            if i == color:
                len_ += 1
                max_len = len_ if len_ > max_len else max_len
            else:
                len_ = 0
    return max_len    

def measure_col(grid: ndarray, color: int) -> int:
    return measure_row(grid.T, color)

def measure_diag(grid: ndarray, color: int) -> int:
    max_len = 0
    for d in range(len(grid)):
        len_ = 0
        for i in range(d, len(grid)):
            for j in range(d, len(grid)):
                if grid[d+i, d+j] == color:
                    len_ += 1
                    max_len = len_ if len_ > max_len else max_len
                else:
                    len_ = 0
    return max_len    


def stone_sum(grid: ndarray, color: int):
    # Returns the difference between the total of black and white stones. The bigger the better.
    return grid.sum() * color

def longest_line(grid: ndarray, color: int):
    # Returns the difference between the longest black and white lines of stones. The bigger the better. 
    black_max = max([measure_row(grid, BLACK), measure_col(grid, BLACK), measure_diag(grid, BLACK)])
    white_max = max([measure_row(grid, WHITE), measure_col(grid, WHITE), measure_diag(grid, WHITE)])
    if color == BLACK:
        return black_max - white_max
    return white_max - black_max

