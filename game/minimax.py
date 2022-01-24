from __future__ import annotations
import numpy as np
from typing import Tuple
import time

from game.board import *
from game.metrics import *

class Solver():
    def __init__(self, depth: int) -> None:
        self.depth = depth
        self.TTtable = {}

    def minimax(self, node: Node, depth: int, maximizingPlayer: bool) -> int:
        if depth == 0 or node.is_terminal():
            return node.score()

        if maximizingPlayer:
            value = float('-inf')
            for child in node.generate_next_moves():
                value = max(value, self.minimax(child, depth-1, ~maximizingPlayer))
                return value

        value = float('inf')
        for child in node.generate_next_moves():
            value = min(value, self.minimax(child, depth-1, maximizingPlayer))
            return value
    
    def minimax_ab_tt(self, node: Node, depth: int, alpha:int, beta:int, maximizingPlayer: bool, starting_color: int) -> int:
        # print(f"minimax | depth = {depth}")
        t1 = time.time()
        hash_ = node.grid.data.tobytes()
        if hash_ in self.TTtable.keys() and starting_color in self.TTtable[hash_].keys():
            if self.TTtable[hash_][starting_color]['depth'] >= depth:
                t2 = time.time()
                # print(f"minimax time = {t2 - t1} | depth = {depth}")
                return self.TTtable[hash_][starting_color]['score']
        
        hash_lst = [hash_, np.rot90(node.grid).data.tobytes(), np.rot90(node.grid, 2).data.tobytes(), 
                        np.flipud(node.grid).data.tobytes(), np.fliplr(node.grid).data.tobytes()]

        if depth == 0 or node.is_terminal():
            t2 = time.time()
            # print(f"minimax time = {t2 - t1} | depth = {depth}")
            return node.score()

        if maximizingPlayer:
            value = float('-inf')
            
            next_moves = node.generate_next_moves()
            while len(next_moves) > 0:
                _, child = next_moves.pop()
                value = max(value, self.minimax_ab_tt(child, depth-1, alpha, beta, False, starting_color))
                alpha = max(value, alpha)
                if alpha >= beta:
                    break
            for h in hash_lst:
                self.TTtable[h] = {}
                self.TTtable[h][starting_color] = {
                    'depth': depth,
                    'score': value
                }
        
            t2 = time.time()
            # print(f"minimax time = {t2 - t1} | depth = {depth}")
            return value
              
        value = float('inf')
        
        next_moves = node.generate_next_moves()
        while len(next_moves) > 0:
            _, child = next_moves.pop()
            value = min(value, self.minimax_ab_tt(child, depth-1, alpha, beta, True, starting_color))
            beta = min(value, beta)
            if alpha >= beta:
                break
            for h in hash_lst:
                self.TTtable[h] = {} # FIXME 
                self.TTtable[h][starting_color] = {
                    'depth': depth,
                    'score': value
                }

        t2 = time.time()
        # print(f"minimax time = {t2 - t1} | depth = {depth}")
        return value

    def minimax_ab(self, node: Node, depth: int, alpha:int, beta:int, maximizingPlayer: bool) -> int:
        if depth == 0 or node.is_terminal():
            return node.score()

        if maximizingPlayer:
            value = float('-inf')
            for child in node.generate_next_moves():
                value = max(value, self.minimax_ab(child, depth-1, alpha, beta, ~maximizingPlayer))
                alpha = max(value, alpha)
                if alpha >= beta:
                    break
            return value

        value = float('inf')
        for child in node.generate_next_moves():
            value = min(value, self.minimax_ab(child, depth-1, alpha, beta, ~maximizingPlayer))
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
        for child in node.generate_next_moves():
            value = max(value, -self.negamax_ab(child, depth-1, -beta, -alpha, -color, starting_color))
            alpha = max(value, alpha)
            if alpha >= beta:
                break
        return value

    def find_best_move(self, current_state: Node) -> Node:
        # print("find best move")
        #t1 = time.time()
        nxt = list(current_state.generate_next_moves())
        #t2 = time.time()
        
        #print(f"next moves len = {len(nxt)} ({t2 -t1} s)")
        
        # minimax will maximize the score for the Black player and minimize the score for the White player.
        #next_moves = [(self.minimax_ab_tt(n, self.depth, float('-inf'), float('inf'), current_state.color == BLACK, n.color * -1), n ) for _, n in nxt]
        
        #next_moves = [(self.minimax(n, self.depth, float('-inf'), float('inf'), current_state.color == BLACK)) for _, n in nxt]
        next_moves = [self.minimax_ab(n, self.depth, float('-inf'), float('inf'), current_state.color != BLACK) for n in nxt]
        #next_moves = [(self.minimax_ab_tt(n, self.depth, float('-inf'), float('inf'), current_state.color == BLACK), n) for _, n in nxt]
        
        #print(next_moves)
        if len(next_moves) != 0:
            if current_state.color != BLACK:
                max_score = max(next_moves)
                #print("max_score = ", max_score)
                #print("where next_moves == max_score = ", np.argwhere(np.array(next_moves) == max_score))
                #print("Best nodes position = ", nxt[np.argwhere(np.array(next_moves) == max_score)[0][0]].current_pos)
                return nxt[np.argwhere(np.array(next_moves) == max_score)[0][0]]
            else:
                min_score = min(next_moves)
                #print("min_score = ", min_score)
                #print("where next_moves == min_score = ", np.argwhere(np.array(next_moves) == min_score)[0])
                #print("Best nodes = ", nxt[np.argwhere(np.array(next_moves) == min_score)[0][0]])
                #print("Best nodes position = ", nxt[np.argwhere(np.array(next_moves) == min_score)[0][0].current_pos])
                return nxt[np.argwhere(np.array(next_moves) == min_score)[0][0]]
            
    def find_best_next_move(self) -> Node:
        """ Return the best next moves for the current player"""
        pass

