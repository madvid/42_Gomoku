from __future__ import annotations
import numpy as np
from board import Node
from typing import Tuple

class Solver():
    def __init__(self, depth: int) -> None:
        self.depth = depth
        self.TTtable = {}

    def minimax(self, node: Node, depth: int, maximizingPlayer: bool, starting_color: int) -> int:
        if depth == 0 or node.is_terminal():
            return node.score(starting_color)

        if maximizingPlayer:
            value = float('-inf')
            for child in node.generate_next_moves(node.color):
                value = max(value, self.minimax(child, depth-1, False))
                return value

        value = float('inf')
        for child in node.generate_next_moves(node.color):
            value = min(value, self.minimax(child, depth-1, True))
            return value
    

    def minimax_ab_tt(self, node: Node, depth: int, alpha:int, beta:int, maximizingPlayer: bool, starting_color: int) -> int:
        hash_ = node.grid.data.tobytes()
        if hash_ in self.TTtable.keys() and starting_color in self.TTtable[hash_].keys():
            if self.TTtable[hash_][starting_color]['depth'] >= depth:
                return self.TTtable[hash_][starting_color]['score']        
        
        hash_lst = [hash_, np.rot90(node.grid).data.tobytes(), np.rot90(node.grid, 2).data.tobytes(), 
                        np.flipud(node.grid).data.tobytes(), np.fliplr(node.grid).data.tobytes()]

        if depth == 0 or node.is_terminal():
            return node.score(starting_color)

        if maximizingPlayer:
            value = float('-inf')
            for child in node.generate_next_moves(node.color):
                value = max(value, self.minimax_ab(child, depth-1, alpha, beta, False, starting_color))
                alpha = max(value, alpha)
                if alpha >= beta:
                    break
            for h in hash_lst:
                self.TTtable[h] = {}
                self.TTtable[h][starting_color] = {
                    'depth': depth,
                    'score': value
                }
            return value

        value = float('inf')
        for child in node.generate_next_moves(node.color):
            value = min(value, self.minimax_ab(child, depth-1, alpha, beta, True, starting_color))
            beta = min(value, beta)
            if alpha >= beta:
                break
            for h in hash_lst:
                self.TTtable[h] = {}
                self.TTtable[h][starting_color] = {
                    'depth': depth,
                    'score': value
                }
        return value

    def minimax_ab(self, node: Node, depth: int, alpha:int, beta:int, maximizingPlayer: bool, starting_color: int) -> int:
        if depth == 0 or node.is_terminal():
            return node.score(starting_color)

        if maximizingPlayer:
            value = float('-inf')
            for child in node.generate_next_moves(node.color):
                value = max(value, self.minimax_ab(child, depth-1, alpha, beta, False, starting_color))
                alpha = max(value, alpha)
                if alpha >= beta:
                    break
            return value

        value = float('inf')
        for child in node.generate_next_moves(node.color):
            value = min(value, self.minimax_ab(child, depth-1, alpha, beta, True, starting_color))
            beta = min(value, beta)
            if alpha >= beta:
                break
        return value


    # def negamax(self, node: Node, depth: int, color: int) -> int:
    #     if depth == 0 or node.is_terminal():
    #         return node.score() * color
    #     value = float('-inf')
    #     for child in node.generate_next_moves(-color):
    #         value = max(value, -self.negamax(child, depth-1, -color))
    #     return value
    

    def negamax_ab(self, node: Node, depth: int, alpha: int, beta: int, color: int, starting_color: int) -> int:
        if depth == 0 or node.is_terminal():
            return node.score(starting_color) * color * -1
        value = float('-inf')
        for child in node.generate_next_moves(node.color):
            value = max(value, -self.negamax_ab(child, depth-1, -beta, -alpha, -color, starting_color))
            alpha = max(value, alpha)
            if alpha >= beta:
                break
        return value

    def find_best_move(self, current_state: Node) -> Node:
        # next_moves = [(self.negamax_ab(n, self.depth, current_state.color * -1, float('-inf'), float('inf'), current_state.color * -1), n ) for n in current_state.generate_next_moves(current_state.color)]
        next_moves = [(self.minimax_ab_tt(n, self.depth, current_state.color == -1, float('-inf'), float('inf'), current_state.color * -1), n ) for n in current_state.generate_next_moves(current_state.color)]
        
        if current_state.color == 1:
            return max(next_moves, key= lambda x: x[0])[1]
        else:
            return min(next_moves, key= lambda x: x[0])[1]

