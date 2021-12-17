
from game.metrics import *
from game.minimax import Solver
from game.board import Node, sum_kern3, sum_mask3

# Node.metric =  {-1: sum_longest, 1: sum_longest}
# Node.metric =  {-1: sum_kern3, 1: sum_mask3}
# g = np.array([
#     [0,  0,  0,  0,  0, 0],
#     [0,  0,  0,  0,  0, 0],
#     [0,  1,  1,  1,  0, 0],
#     [0,  0,  0,  0, -1, 0],
#     [0,  0,  0,  0, -1, 0],
#     [0,  0,  0,  0, -1, 0]
#     ])

g = np.zeros((27,27))
sb = np.zeros((27,27))
g[13][13] = 1
parent = Node(None, g, -1, pos = (5,5))

color = 1
node = Node(parent, g, color, pos = (13,13))
solver = Solver(1)

# print(solver.find_best_move(node))

for _ in range(10):
    node = solver.find_best_move(node)
    print('------------')
    print(f'color: {node.color* -1} | best score: {node.score(node.color)}')    
    print(node.grid[4:-4, 4:-4].astype('int8'))
    print('------------')