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
assets = {"button cancel": "assets/Cancel.png"}
dct_stylesheet ={"cancel_btn": "*{border: 0px solid '#FFCCCC';" +
                 "border-radius: 20px;" +
                 "font-size: 20px;" +
                 "color: white;" +
                 "padding: 0px 0px;" +
                 "margin: 0px 0px;}" +
                 "*:hover{background: '#FF6666';}"}

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

    def remove_stone(self, idx, color):
        idx.reverse()
        print(f" ___ idx ___ = {idx}")
        if color == "white":
            for ii in idx:
                print(ii)
                self.whitestone[ii][0].deleteLater()
                del(self.whitestone[ii])
        if color == "black":
            for ii in idx:
                print(ii)
                self.blackstone[ii][0].deleteLater()
                del(self.blackstone[ii])

    def update_board(self, color:int):
        """ Update the board after the player/IA played.
        Update is called to remove stone which has been captured.
        Args:
        -----
            color ([int]): color of the last stone put on the board
        Amelioration:
        -------------
        Possibilité de simplifier la fonction si whitestone et blackstone
        sont dans un dictionnaire avec comme clef "white" et "black"
        """
        l_remove = []
        if color == 1: # white
            for ii, stone in enumerate(self.blackstone):
                if self.grid[stone[1][0], stone[1][1]] == 0:
                    l_remove.append(ii)
            self.remove_stone(l_remove, "black")
        if color == -1: # black
            for ii, stone in enumerate(self.whitestone):
                if self.grid[stone[1][0], stone[1][1]] == 0:
                    l_remove.append(ii)
            self.remove_stone(l_remove, "white")
            
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
            coord = stone_to_board(nearest, self.stone, self.grid)
        else:
            nearest = nearest_coord(event)[::-1]
            coord = (event - 26) / 31
        if color == 1:
            self.whitestone.append((current_stone, coord.astype('int8')))
        else:
            self.blackstone.append((current_stone, coord.astype('int8')))
        
        current_stone.move(nearest[0] - 26, nearest[1] - 26)
        current_stone.show()

    #def stack3UI(self):
    #    super(GameUI).stack3UI()
    #    self.wdgts_UI3["button cancel"].setIcon(QtGui.QIcon(assets["button cancel"]))
    #    self.wdgts_UI3["button cancel"].setIconSize(QtCore.QSize(203,67))
    #    self.wdgts_UI3["button cancel"].setStyleSheet(dct_stylesheet["cancel_btn"])
    #    self.wdgts_UI3["button cancel"].clicked.connect(self.game_cancel)
    #    grid.addWidget(self.wdgts_UI3["button cancel"], 4, 2, 1, 2)

    def game_cancel(self):
        pass
        #self.Stack.setCurrentIndex(0)

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
            self.placing_stone(event, self.stone)
            self.update_board(self.stone)

            self.node = Node(self.node, self.grid, color=-self.stone)
            self.stone = self.node.color

            self.node = self.agent.find_best_move(self.node)
            prev_grid = self.grid
            self.grid = self.node.grid
            dgrid = prev_grid - self.grid
            coord = 31 * (np.argwhere(dgrid != 0)[0]) + 26
            
            self.placing_stone(coord, self.stone)
            self.update_board(self.stone)
            self.stone *= -1

