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
        
        rm_funcs = {
            Row: remove_row,
            Column: remove_col,
            Diagonal: remove_diag
        }

        for seq in sequences:
            grid = rm_funcs[type(seq)](grid)
        
        return grid


    def generate_next_moves(self) -> List[Node]:
        possibles_moves_idx = np.argwhere(self.grid == 0)
        possibles_moves = [self.update((x,y), self.color * -1) for x,y in possibles_moves_idx]

        # TODO: Remove any node where the new stone is captured
        # For each node:
        # 1. Collect all stones sequences for black and white
        # 2. Remove any surrounded  black or white sequences from the board
        # 3. Check for double free-three
        for m in possibles_moves:
            stone_seq: List[StoneSequence] = collect_sequences(m.grid, BLACK) + collect_sequences(m.grid, WHITE)

            # Captured stones
            captured_stones = filter(lambda x: x.length == 2 and x.is_surrounded(), stone_seq)
            m.grid = self.remove_sequences(m.grid, captured_stones)

            # Double free-three
            cleared_stone_seq: List[StoneSequence] = collect_sequences(m.grid, BLACK) + collect_sequences(m.grid, WHITE)
            grouped_free_three = filter(lambda x: x.length == 3 and x.have_two_freedom(), cleared_stone_seq)

        
            # TODO: Check double free-three
            # Get all availables moves
            # For each:
            # 1. collect possible moves from there (with same color played)
            # 2. For each:
            #   Collect availables moves.
            #   If at least one move contains two StoneSequences of length == 4, discard the move.  
            available_moves =  filter(lambda x : ~ (x.length == 2 and x.is_surrounded()), stone_seq)
            for a in available_moves:
                next_moves_idx = np.argwhere(a.grid == 0)
                next_moves = [self.update((x,y), self.color) for x,y in next_moves_idx]
                for i, n in enumerate(next_moves):
                    n_seq: List[StoneSequence] = collect_sequences(n.grid, BLACK) + collect_sequences(n.grid, WHITE)
                    if len(filter(lambda x : x.length == 4, n_seq)) >= 2:
                        available_moves.remove(a)
            # TODO: Verify that !!
        
            for 
        return possibles_moves

    def score(self) -> int:
        return Node.metric[self.color](self.grid, self.color)