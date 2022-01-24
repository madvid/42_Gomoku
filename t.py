
from game.metrics import *
from game.minimax import Solver
from game.board import Node, sum_kern3, sum_mask3
np.set_printoptions(linewidth = 200)

np.set_printoptions(linewidth = 200)

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
#g[[13, 14, 15, 16, 17], [13,14, 15, 16, 17]] = 1
#g[[14, 15, 16, 17],[14, 15, 16, 17]] = -1
parent = Node(None, g, -1, pos = (5,5))

color = 1
g[13,13] = color
node = Node(parent, g, color, pos = (13,13))
# color = -1
# g[18,18] = color
# node2 = Node(node1, g, color, pos = (18,18))

# print(node2.grid)

# assert(node2.is_terminal())


solver = Solver(2)


# print(node.grid.astype('int8'))
# print(node.color)

# print(solver.find_best_move(node).grid.astype('int8'))
# print(solver.find_best_move(node).color)

for _ in range(10):
    node = solver.find_best_move(node)
    print('------------')
    print(f'color: {node.color} | best score: {node.score()}')    
    print(f'pos: {node.current_pos}')    
    print(node.grid[4:-4, 4:-4].astype('int8'))
    print('scoreboard')
    print(node.scoreboard[node.color][4:-4, 4:-4].astype('int8'))
    print('------------')