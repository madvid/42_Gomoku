# =========================================================================== #
# ____________________  |Importation des lib/packages|   ____________________ #
# =========================================================================== #
from interface.game_interface import MyWindow
from game.minimax import Solver
from game.board import Node
import numpy as np
from __future__ import annotations

# =========================================================================== #
#                          | constants definition |                           #
# =========================================================================== #


# =========================================================================== #
#                          | fonctions definition |                           #
# =========================================================================== #

	

# =========================================================================== #
#                           | Classes definition |                            #
# =========================================================================== #
class Game():
	def __init__(self):
		# Board creation, common for mywindow object and the Solver object
		self.grid = np.zeros((19,19), dtype=np.int8)
		
		# instance of MyWindow = the UI object
		self.mywindow = MyWindow()
		
		# instance of Solver = generate the accessible moves from current node
		self.agent = Solver(depth=1)
		
		# Initialization of the tree.
		parent = Node(None, self.grid, -1)
		parent.nb_free_three = 0
		self.node = Node(parent, self.grid, color=1)
