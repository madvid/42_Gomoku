# =========================================================================== #
# ____________________  |Importation des lib/packages|   ____________________ #
# =========================================================================== #
from __future__ import annotations
import numpy as np
#from board import Node

# =========================================================================== #
# ___________________________    |CONSTANTES|    ____________________________ #
# =========================================================================== #


# =========================================================================== #
# ___________________________    |FUNCTIONS|     ____________________________ #
# =========================================================================== #


# =========================================================================== #
# ___________________________     |CLASSES|      ____________________________ #
# =========================================================================== #

class BoardConfig():
	ROUND = 0

	def __init__(self,player:int, count_round=True):
		self.coordinates = {"white": None,
							"black": None
							}
		self.who_played = player
		if count_round:
			self.round = self.ROUND + 1
			self.ROUND += 1


	def add_coordinates_stones(self, coordinates:np.array, color:int):
		if (coordinates.ndim) != 2 or coordinates.shape[1] != 2:
			raise ValueError("coordinates has wrong shape: expected (x, 2).")

		if color == 1: #white player
			if self.coordinates["white"] is None:
				self.coordinates["white"] = coordinates
			else:
				np.append(self.coordinates["white"], coordinates, axis=0)
		if color == -1: #black player
			if self.coordinates["black"] is None:
				self.coordinates["black"] = coordinates
			else:
				np.append(self.coordinates["black"], coordinates, axis=0)


	def _coord2board(self) -> np.array:
		board = np.zeros((19,19), dtype=np.int8)
		c = self.coordinates
		board[np.ix_(c["white"][:,0], c["white"][:,1])] = 1
		board[np.ix_(c["black"][:,0], c["black"][:,1])] = -1
		return board


	def boardconfig2node(self) -> Node:
		node = Node(parent=None, grid=self._coord2board(), color=self.who_played)
		return node


class History():
	def __init__(self):
		self.history = []
		self.i_current = -1


	def catch_coordinates(self, board:np.array, color:int) -> np.array:
		xy_stones = np.argwhere(board == color)
		return xy_stones


	def node2boardconfig(self, node:Node) -> BoardConfig:
		current_player = node.color
		new_config = BoardConfig(current_player, count_round=False)
		black_coordinates = self.catch_coordinates(node.grid, -1)
		white_coordinates = self.catch_coordinates(node.grid, 1)
		new_config.add_coordinates_stones(black_coordinates, -1)
		new_config.add_coordinates_stones(white_coordinates, 1)
		return new_config


	def add_nodes(self, l_node:List[Node]):
		for n in l_node:
			bc = self.node2boardconfig(n)
			self.history.append(bc)
			self.i_current += 1


	def explore_history(self,shift:int):
		if not shift in [-1, 1]:
			raise ValueError("Argument shift must only be 1 or -1.")
		if self.i_current == 0:
			raise ValueError("History is at the beginning already.")
		if self.i_current == len(self.history) + 1:
			raise ValueError("History is at the end already.")
		self.i_current += shift
