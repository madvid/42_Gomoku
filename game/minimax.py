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
            for child in node.generate_next_moves():
                value = max(value, self.minimax(child, depth-1, False))
                return value

        value = float('inf')
        for child in node.generate_next_moves():
            value = min(value, self.minimax(child, depth-1, True))
            return value
    
    def minimax_ab(self, node: Node, depth: int, alpha:int, beta:int, maximizingPlayer: bool) -> int:
        if depth == 0 or node.is_terminal():
            return node.score()

        if maximizingPlayer:
            value = float('-inf')
            for child in node.generate_next_moves():
                value = max(value, self.minimax(child, depth-1, alpha, beta, False))
                alpha = max(value, alpha)
                if alpha >= beta:
                    break
            return value

        value = float('inf')
        for child in node.generate_next_moves():
            value = min(value, self.minimax(child, depth-1, alpha, beta, True))
            beta = min(value, beta)
            if alpha >= beta:
                break
        return value

    def negamax(self, node: Node, depth: int, color: int) -> int:
        if depth == 0 or node.is_terminal():
            return node.score() * color
        value = float('-inf')
        for child in node.generate_next_moves():
            value = max(value, -self.negamax(child, depth-1, -color))
        return value
    

    def negamax_ab(self, node: Node, depth: int, alpha: int, beta: int, color: int) -> int:
        if depth == 0 or node.is_terminal():
            return node.score() * color
        value = float('-inf')
        for child in node.generate_next_moves():
            value = max(value, -self.negamax(child, depth-1, -beta, -alpha, -color))
            alpha = max(value, alpha)
            if alpha >= beta:
                break
        return value

    def find_best_move(self, current_state: Node) -> Node:
        maximizing = current_state.color == 1
        next_moves = [(self.minimax(n, self.depth, maximizing), n) for n in current_state.generate_next_moves()]
        if maximizing:
            return max(next_moves)[1]
        return min(next_moves)[1]
