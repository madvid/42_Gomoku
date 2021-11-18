
from metrics import *
from minimax import Solver
from board import Node

# Node.metric =  {-1: sum_longest, 1: sum_longest}
Node.metric =  {-1: sum_mask3, 1: sum_mask3}
g = np.array([
    [0,  0,  0,  0,  0, 0],
    [0,  0,  0,  0,  0, 0],
    [0,  1,  1,  1,  0, 0],
    [0,  0,  0,  0, -1, 0],
    [0,  0,  0,  0, -1, 0],
    [0,  0,  0,  0, -1, 0]
    ])
parent = Node(None, g, -1)
parent.nb_free_three = 0

color = 1
node = Node(parent, g, color)
solver = Solver(1)

for _ in range(10):
    node = solver.find_best_move(node)
    print('------------')
    print(f'color: {node.color} | best score: {node.score()}')    
    print(node.grid)
    print('------------')



