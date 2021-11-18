# =========================================================================== #
# ____________________  |Importation des lib/packages|   ____________________ #
# =========================================================================== #
from interface.game_interface import mywindow
from game.minimax import solver
from game.board import Node
import numpy as np
from __future__ import annotations

# =========================================================================== #
#                          | constants definition |                           #
# =========================================================================== #


# =========================================================================== #
#                          | fonctions definition |                           #
# =========================================================================== #

def initiate_instance(g:Game):
	parent = Node(None, g, -1)
	g.parent.nb_free_three = 0
	color = 1
	node = Node(parent, g, color)
	

# =========================================================================== #
#                           | Classes definition |                            #
# =========================================================================== #
class Game():
	def __init__(self):
		self.grid = np.zeros((19,19))
		self.mywindow = mywindow()
		self.agent = solver()
