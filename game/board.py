from __future__ import annotations
import numpy as np
import copy
from typing import Tuple, List

from metrics import * 

class Node():
    # Global attributes of all nodes. Generated once before building the tree.
    metric: dict = {} # A dict containing the scoring metrics for black and white
        
    def __init__(self, parent: Node, grid: np.ndarray, color: int) -> None:
        self.parent = parent
        self.grid = grid
        self.color = color
        self.nb_free_three = None # Attribute updated after the creation of the instance.
    
    def is_terminal(self):
        # FIXME
        return False

    def update(self, pos: Tuple[int,int], color: int) -> Node:
        tmp_grid = np.copy(self.grid)
        tmp_grid[pos] = color
        return Node(self, tmp_grid, color)

    def remove_sequences(self, grid: np.ndarray, sequences: List[StoneSequence]) -> np.ndarray:
        def remove_row(grid: np.ndarray, row: Row):
            for i in range(row.length):
                grid[row.start[0], row.start[1] + i] = 0
            return grid
        
        def remove_col(grid: np.ndarray, col: Column):
            for i in range(col.length):
                grid[col.start[0] + i, col.start[1]] = 0
            return grid

        def remove_diag(grid: np.ndarray, diag: Diagonal):
            for i in range(diag.length):
                if diag.left:
                    grid[diag.start[0] + i, diag.start[1] + i] = 0
                else:
                    grid[diag.start[0] + i, diag.start[1] - i] = 0
            return grid
        
        rm_funcs = {
            Row: remove_row,
            Column: remove_col,
            Diagonal: remove_diag
        }
        for seq in sequences:
            tmp_grid = copy.deepcopy(grid)
            tmp_grid = rm_funcs[type(seq)](tmp_grid, seq)
            grid = tmp_grid
        return grid


    def generate_next_moves(self, color: int) -> List[Node]:
        possibles_moves_idx = np.argwhere(self.grid == 0)
        possibles_moves = [self.update((x,y), color) for x,y in possibles_moves_idx]
        for m in possibles_moves:
            stone_seq: List[StoneSequence] = collect_sequences(m.grid, BLACK) + collect_sequences(m.grid, WHITE)
            # Captured stones
            captured_stones = filter(lambda x: x.length == 2 and x.is_surrounded(), stone_seq)
            # print(f"captured = {captured_stones[0].grid}")
            m.grid = self.remove_sequences(m.grid, captured_stones)

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

    def score(self) -> int:
        return Node.metric[self.color](self.grid) #, self.color)