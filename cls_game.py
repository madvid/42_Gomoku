# =========================================================================== #
# ____________________  |Importation des lib/packages|   ____________________ #
# =========================================================================== #
from __future__ import annotations

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, \
	QVBoxLayout, QWidget, QGridLayout, QStackedWidget, QHBoxLayout, QVBoxLayout
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QCursor

from interface.game_interface import MyWindow, nearest_coord, stone_to_board
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

	def mousePressEvent(self, event):
		#if (self.Stack.currentIndex() == 2):
		#	super(GameUI, self).mouseMoveEvent(self.event)
		def on_board(qpoint):
			x, y = qpoint.x(), qpoint.y()
			if (x >= 25) and (x <= 603) and (y >= 25) and (y <= 603):
				return True
			return False


		if (self.Stack.currentIndex() == 2) and on_board(event.pos()) and (event.buttons() == QtCore.Qt.LeftButton):
			
			current_stone =  QLabel("", self.wdgts_UI3["board"])
			current_stone.setStyleSheet("background-color: transparent;")
			# Creer un evenement de placement pour qu'il puisse etre appelé par l'algo
			if self.stone == 1:
				px_stone = QPixmap("assets/stone_white.png")
				px_stone = px_stone.scaled(26, 26, QtCore.Qt.KeepAspectRatio)
				current_stone.setPixmap(px_stone)
				self.whitestone.append(current_stone)
			else:
				px_stone = QPixmap("assets/stone_black.png")
				px_stone = px_stone.scaled(26, 26, QtCore.Qt.KeepAspectRatio)
				current_stone.setPixmap(px_stone)
				self.blackstone.append(current_stone)

			print(f"coordinates mouse: {event.pos().x()}, {event.pos().y()}")
			nearest = nearest_coord(np.array([event.pos().x(), event.pos().y()]))
			#print(nearest)
			
			if not hasattr(self, 'grid'):
				self.grid = np.zeros((19,19))
			stone_to_board(nearest, self.stone, self.grid)
			current_stone.move(int(1.02 * nearest[0]) - 26, int(1.02 * nearest[1]) - 26)
			current_stone.show()

			self.node = Node(self.node, self.grid, color=-self.stone)

			print("before")
			self.node = self.agent.find_best_move(self.node)
			prev_grid = self.grid
			self.grid = self.node.grid
			print(self.grid)
			dgrid = prev_grid - self.grid
			coord = 31 * (np.argwhere(dgrid != 0) + 1)
			
			print("coord:", coord)			
			stone_to_board(coord[0], self.stone, self.grid)
			
			ia_stone =  QLabel("", self.wdgts_UI3["board"])
			ia_stone.setStyleSheet("background-color: transparent;")
			
			if self.node.color == 1:
				px_stone = QPixmap("assets/stone_white.png")
				px_stone = px_stone.scaled(26, 26, QtCore.Qt.KeepAspectRatio)
				ia_stone.setPixmap(px_stone)
				self.whitestone.append(ia_stone)
			else:
				px_stone = QPixmap("assets/stone_black.png")
				px_stone = px_stone.scaled(26, 26, QtCore.Qt.KeepAspectRatio)
				ia_stone.setPixmap(px_stone)
				self.blackstone.append(ia_stone)
			
			ia_stone.move(int(1.02 * coord[0][1]) - 26, int(1.02 * coord[0][0]) - 26)
			ia_stone.show()







