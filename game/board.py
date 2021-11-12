from __future__ import annotations
import numpy as np
from typing import Tuple, List

from metrics import * 

class Node():
    # Global attributes of all nodes. Generated once before building the tree.
    metric = None # A dict containing the scoring metrics for black and white
        
    def __init__(self, parent: Node, grid: np.ndarray, color: int = BLACK) -> None:
        self.parent = parent
        self.grid = grid
        self.color = color
    
    def are_surounded(self) -> np.ndarray:
        # Returns an array of bools. 
        pass

    def update(self, pos: Tuple[int,int], color: int) -> Node:
        tmp_grid = np.copy(self.grid)
        tmp_grid[pos] = color
        return Node(self, tmp_grid, color)

    def generate_next_moves(self) -> List[Node]:
        possibles_moves = np.nonzero(self.grid == 0)
        return [self.update((x,y), self.color * -1) for x,y in zip(*possibles_moves)]

    def score(self) -> int:
        return Node.metric[self.color](self.grid, self.color)