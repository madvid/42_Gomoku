import numpy as np
from numpy import ndarray
from typing import Tuple, List
from __future__ import annotations

# Position = NamedTuple[int,int]

class Node():
    # Global attributes of all nodes
    grid_shape = None
    
    def __init__(self, grid: ndarray, color: int = 1) -> None:
        self.grid = grid
        self.color = color
    
    def update(self, pos: Tuple[int,int], color: int = 1) -> Node:
        tmp_grid = np.deepcopy(self.grid)
        tmp_grid[pos] = color
        return Node(tmp_grid)

    def generate_next_moves(self) -> List[Node]:
        possibles_moves = np.argwhere(self.grid == 0)
        return [self.update(pos, self.color * -1) for pos in possibles_moves]