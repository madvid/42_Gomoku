# =========================================================================== #
# ____________________  |Importation des lib/packages|   ____________________ #
# =========================================================================== #
from __future__ import annotations

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, \
	QVBoxLayout, QWidget, QGridLayout, QStackedWidget, QHBoxLayout, QVBoxLayout
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QCursor

from interface.game_interface import MyWindow, nearest_coord, stone_to_board, assets
from game.minimax import Solver
from game.board import Node
import numpy as np

# =========================================================================== #
#                          | constants definition |                           #
# =========================================================================== #


# =========================================================================== #
#                          | fonctions definition |                           #
# =========================================================================== #

	

# =========================================================================== #
#                           | Classes definition |                            #
# =========================================================================== #
class GameUI(MyWindow):
	def __init__(self, gmode:int):
		super(GameUI, self).__init__()
		# Board creation, common for mywindow object and the Solver object
		self.grid = np.zeros((5,5), dtype=np.int8)
		
		# instance of Solver = generate the accessible moves from current node
		self.agent = Solver(depth=1)
		
		# Initialization of the tree.
		parent = Node(None, self.grid, -1)
		parent.nb_free_three = 0
		self.node = Node(parent, self.grid, color=-self.stone)

		self.gamemode = gmode
		if self.gamemode == 1:
			self.p1_type = 'Human'
			self.p2_type = 'Human'
		elif self.gamemode == 2:
			self.p1_type = 'Human'
			self.p2_type = 'IA'
		elif self.gamemode == 3:
			self.p1_type = 'IA'
			self.p2_type = 'IA'
		
		self.i_round = 0

	def placing_stone(self, event, color):
		current_stone =  QLabel("", self.wdgts_UI3["board"])
		current_stone.setStyleSheet("background-color: transparent;")
		
		if color == 1: #white
			px_stone = QPixmap(assets["white_stone"])
		else:
			px_stone = QPixmap(assets["black_stone"])
		px_stone = px_stone.scaled(26, 26, QtCore.Qt.KeepAspectRatio)
		current_stone.setPixmap(px_stone)

		if isinstance(event, QtGui.QMouseEvent):
			nearest = nearest_coord(np.array([event.pos().x(), event.pos().y()]))
		else:
			nearest = nearest_coord(event)
		stone_to_board(nearest, self.stone, self.grid)
		current_stone.move(int(1.02 * nearest[0]) - 26, int(1.02 * nearest[1]) - 26)
		return current_stone

	def mousePressEvent(self, event):
		def on_board(qpoint):
			x, y = qpoint.x(), qpoint.y()
			if (x >= 25) and (x <= 603) and (y >= 25) and (y <= 603):
				return True
			return False

		if (self.Stack.currentIndex() == 2) and on_board(event.pos()) and (event.buttons() == QtCore.Qt.LeftButton):
			if not hasattr(self, 'grid'):
				self.grid = np.zeros((19,19))
			
			# Creer un evenement de placement pour qu'il puisse etre appelé par l'algo
			current_stone = self.placing_stone(event, self.stone)
			if self.stone == 1:
				self.whitestone.append(current_stone)
			else:
				self.blackstone.append(current_stone)
			current_stone.show()
			self.stone = -self.stone

			self.node = Node(self.node, self.grid, color=self.stone)

			self.node = self.agent.find_best_move(self.node)
			prev_grid = self.grid
			self.grid = self.node.grid
			dgrid = prev_grid - self.grid
			coord = 31 * (np.argwhere(dgrid != 0)[0] + 1) + 26
			
			ia_stone = self.placing_stone(coord, self.stone)		
			if self.stone == 1:
				self.whitestone.append(ia_stone)
			else:
				self.blackstone.append(ia_stone)
			ia_stone.show()






