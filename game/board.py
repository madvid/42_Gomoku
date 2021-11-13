from __future__ import annotations
import numpy as np
from typing import Tuple, List

from metrics import * 

class Node():
    # Global attributes of all nodes. Generated once before building the tree.
    metric: dict = {} # A dict containing the scoring metrics for black and white
        
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

    def remove_sequences(self, grid: np.ndarray, sequences: List[StoneSequence]) -> np.ndarray:
        pass
        # FIXME


    def generate_next_moves(self) -> List[Node]:
        possibles_moves_idx = np.argwhere(self.grid == 0)
        possibles_moves = [self.update((x,y), self.color * -1) for x,y in possibles_moves_idx]

        # TODO: Remove any node where the new stone is captured
        # For each node:
        # 1. Collect all stones sequences for black and white
        # 2. Remove any surrounded  black or white sequences from the board
        # 3. Check for double free-three
        for m in possibles_moves:
            black_stone_seq = collect_sequences(m.grid, BLACK)
            white_stone_seq = collect_sequences(m.grid, WHITE)

            # Captured stones
            captured_stones = filter(lambda x : x.length == 2 and x.is_surrounded(), black_stone_seq + white_stone_seq)

        
            # TODO: Check double free-three
        return possibles_moves

    def score(self) -> int:
        return Node.metric[self.color](self.grid, self.color)