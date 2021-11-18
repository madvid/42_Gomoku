from __future__ import annotations
import numpy as np
from board import Node
from typing import Tuple

class Solver():
    def __init__(self, depth: int) -> None:
        self.depth = depth

    def minimax(self, node: Node, depth: int, maximizingPlayer: bool) -> int:
        if depth == 0 or node.is_terminal():
            return node.score()

        if maximizingPlayer:
            value = float('-inf')
            for child in node.generate_next_moves(node.color):
                value = max(value, self.minimax(child, depth-1, False))
                return value

        value = float('inf')
        for child in node.generate_next_moves(node.color):
            value = min(value, self.minimax(child, depth-1, True))
            return value
    
    def minimax_ab(self, node: Node, depth: int, alpha:int, beta:int, maximizingPlayer: bool) -> int:
        if depth == 0 or node.is_terminal():
            return node.score()

        if maximizingPlayer:
            value = float('-inf')
            for child in node.generate_next_moves(node.color):
                value = max(value, self.minimax_ab(child, depth-1, alpha, beta, False))
                alpha = max(value, alpha)
                if alpha >= beta:
                    break
            return value

        value = float('inf')
        for child in node.generate_next_moves(node.color):
            value = min(value, self.minimax_ab(child, depth-1, alpha, beta, True))
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
    

    # def negamax_ab(self, node: Node, depth: int, alpha: int, beta: int, color: int) -> int:
    #     if depth == 0 or node.is_terminal():
    #         return node.score() * color
    #     value = float('-inf')
    #     for child in node.generate_next_moves(color):
    #         value = max(value, -self.negamax_ab(child, depth-1, -beta, -alpha, -color))
    #         alpha = max(value, alpha)
    #         if alpha >= beta:
    #             break
    #     return value

    def find_best_move(self, current_state: Node) -> Node:
        # next_moves = [(self.negamax_ab(n, self.depth, current_state.color, float('-inf'), float('inf')), n ) for n in current_state.generate_next_moves(current_state.color)]
        next_moves = [(self.minimax_ab(n, self.depth, current_state.color == 1, float('-inf'), float('inf')), n ) for n in current_state.generate_next_moves(current_state.color)]
        return max(next_moves, key= lambda x: x[0] * current_state.color)[1]
