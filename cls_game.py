# =========================================================================== #
# ____________________  |Importation des lib/packages|   ____________________ #
# =========================================================================== #
from __future__ import annotations

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, \
    QVBoxLayout, QWidget, QGridLayout, QStackedWidget, QHBoxLayout, QVBoxLayout
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QCursor

from typing import Tuple, List
import numpy as np
from numpy.lib.stride_tricks import as_strided

from interface.game_interface import MyWindow, nearest_coord, stone_to_board, assets
from game.minimax import Solver
from game.board import Node
from game.history import History


# =========================================================================== #
#                          | constants definition |                           #
# =========================================================================== #
from constants import WHITE, BLACK, k_diags, k_lines, k_captures, k_free_threes

TOT = 0

dct_stylesheet ={"cancel_btn": "*{border: 0px solid '#FFCCCC';" +
                 "border-radius: 20px;" +
                 "font-size: 20px;" +
                 "color: white;" +
                 "padding: 0px 0px;" +
                 "margin: 0px 0px;}" +
                 "*:hover{background: '#FF6666';}"}

SIZE = 6


# =========================================================================== #
#                          | fonctions definition |                           #
# =========================================================================== #

def current_coordinates(pos:QtCore.QPoint) -> np.array:
    """Returns the index on the grid corresponding to the cursor position.
    Args:
    -----
        pos (QtGui.QMouseEvent): coordinates of the mouse cursor.

    Returns:
    --------
        np.array: indexes (# of line and # of the column).
    """
    nearest = nearest_coord(np.array([pos.x(), pos.y()]))
    coord = np.array([(nearest[1] // 31) - 1, (nearest[0] // 31) - 1])
    return coord


# =========================================================================== #
#                           | Classes definition |                            #
# =========================================================================== #
class GameUI(MyWindow):
    def __init__(self, gmode:int):
        super(GameUI, self).__init__()
        # Board creation and player related attributes
        self.grid = np.zeros((SIZE,SIZE), dtype=np.int8)
        self.W_whitestones = []
        self.W_blackstones = []
        self.coord_whitestones = []
        self.coord_blackstones = []
        self.p1_score = 0
        self.p2_score = 0

        # instance of Solver = generate the accessible moves from current node
        self.agent = Solver(depth=1)
        
        # Initialization of the tree.
        parent = Node(None, self.grid, BLACK)
        parent.nb_free_three = 0
        self.node = Node(parent, self.grid, color=-self.stone)

        self.i_round = 0
        self.history = History()

        
    def game_backward(self):
        """[summary]
        """
        if self.history.i_current > 0:
            self.history.i_current -= 1
            self.grid = self.history.lst_nodes[self.history.i_current]
            self.UiDestroyBoard()
            self.UiGenBoard()


    def game_forward(self):
        """[summary]
        """
        if self.history.i_current + 1 < self.history.tot_nodes:
            self.history.i_current += 1
            self.grid = self.history.lst_nodes[self.history.i_current]
            self.UiDestroyBoard()
            self.UiGenBoard()


    def game_score(self, scores: Tuple[int]):
        """[summary]
        """
        self.p1_score += scores[0]
        self.p2_score += scores[1]
        self.wdgts_UI3["score p1"].setPixmap(QPixmap(assets[f"img_{self.p1_score}"]))
        self.wdgts_UI3["score p2"].setPixmap(QPixmap(assets[f"img_{self.p2_score}"]))
        

    @staticmethod
    def _subboard_4_Conv2D(grid, k_shape:tuple, stride:tuple) -> np.array:
        """ Generates the sub view of the grid to be multiply with the kernel.
        First the shape of the sub_grid array is calculated, it depends on
        the grid shape and the kernel shape.
        The sub_grid array shape will be (n_x, n_y, k_x, k_y) with:
            * n_x: number of application of the kernel along row (with stride of 1)
            * n_y: number of application of the kernel along column (with stride of 1)
            * k_x, k_y: the shape of the kernel
        In this way sub_grid is a numpy array of n_x/n_y rows/columns of (k_x x k_y)
        sub view of the grid.
        Args:
        -----
            k_shape ([tuple[int]]): shape of the kernel
            stride ([tuple(int)]): put self.grid.strides * 2 (but why?)
        """
        view_shape = tuple(np.subtract(grid.shape, k_shape) + 1) + k_shape
        sub_grid = as_strided(grid, view_shape, stride * 2)
        return sub_grid


    @staticmethod
    def _my_conv2D(grid, kernel:np.array) -> np.array:
        """ Retrieves the sub_grid from the function _subboard_4_Conv2D and performs
        the convolution (array multiplication + einstein sum along the 3rd and 4th
        dimensions).
        Args:
        -----
            * kernel ([np.array]): the kernel to use for convolution.
        """
        sub_grid = GameUI._subboard_4_Conv2D(grid, k_shape=kernel.shape, stride=grid.strides)
        res_conv = np.multiply(sub_grid, kernel)
        convolved = np.einsum('ijkl->ij', res_conv)
        return convolved


    def check_board(self):
        """[summary]
        """
        ## Checking if white pair captured
        # Checking the diagonal:
        conv_diag1 = GameUI._my_conv2D(self.grid, k_diags[0])
        conv_diag2 = GameUI._my_conv2D(self.grid, k_diags[1])
        # Checking vertical and horizontal
        conv_lin1 = GameUI._my_conv2D(self.grid, k_lines[0])
        conv_lin2 = GameUI._my_conv2D(self.grid, k_lines[1])
        
        coord_cd1 = np.argwhere(conv_diag1 == 4)
        coord_cd2 = np.argwhere(conv_diag2 == 4)
        coord_cl1 = np.argwhere(conv_lin1 == 4)
        coord_cl2 = np.argwhere(conv_lin2 == 4)
        #print("||||||||||||||||||||||||||||")
        #print("conv_diag1:\n", conv_diag1)
        #print("conv_diag2:\n", conv_diag2)
        #print("conv_lin1:\n", conv_lin1)
        #print("conv_lin2:\n", conv_lin2)
        #print("|||||||||||||||||||||||||||||")

        if coord_cd1.shape[0] != 0:
            for coord in coord_cd1:
                self.grid[coord[0] + 1][coord[1] + 1] = 0
                self.grid[coord[0] + 2][coord[1] + 2] = 0
        if coord_cd2.shape[0] != 0:
            for coord in coord_cd2:
                self.grid[coord[0] + 1][coord[1] + 2] = 0
                self.grid[coord[0] + 2][coord[1] + 1] = 0
        if coord_cl1.shape[0] != 0:
            for coord in coord_cl1:
                self.grid[coord[0]][coord[1] + 1] = 0
                self.grid[coord[0]][coord[1] + 2] = 0
        if coord_cl2.shape[0] != 0:
            for coord in coord_cl2:
                self.grid[coord[0] + 1][coord[1]] = 0
                self.grid[coord[0] + 2][coord[1]] = 0
        ## Checking if black pair captured
        # Checking the diagonal:
        conv_diag1 = GameUI._my_conv2D(self.grid, -1 * k_diags[0])
        conv_diag2 = GameUI._my_conv2D(self.grid, -1 * k_diags[1])
        # Checking vertical and horizontal
        conv_lin1 = GameUI._my_conv2D(self.grid, -1 * k_lines[0])
        conv_lin2 = GameUI._my_conv2D(self.grid, -1 * k_lines[1])

        #print("|||||||||||||||||||||||||||||")
        #print("conv_diag1:\n", conv_diag1)
        #print("conv_diag2:\n", conv_diag2)
        #print("conv_lin1:\n", conv_lin1)
        #print("conv_lin2:\n", conv_lin2)
        #print("|||||||||||||||||||||||||||||")
        
        coord_cd1 = np.argwhere(conv_diag1 == 4)
        coord_cd2 = np.argwhere(conv_diag2 == 4)
        coord_cl1 = np.argwhere(conv_lin1 == 4)
        coord_cl2 = np.argwhere(conv_lin2 == 4)
        if coord_cd1.shape[0] != 0:
            for coord in coord_cd1:
                self.grid[coord[0] + 1][coord[1] + 1] = 0
                self.grid[coord[0] + 2][coord[1] + 2] = 0
        if coord_cd2.shape[0] != 0:
            for coord in coord_cd2:
                self.grid[coord[0] + 1][coord[1] + 2] = 0
                self.grid[coord[0] + 2][coord[1] + 1] = 0
        if coord_cl1.shape[0] != 0:
            for coord in coord_cl1:
                self.grid[coord[0]][coord[1] + 1] = 0
                self.grid[coord[0]][coord[1] + 2] = 0
        if coord_cl2.shape[0] != 0:
            for coord in coord_cl2:
                self.grid[coord[0] + 1][coord[1]] = 0
                self.grid[coord[0] + 2][coord[1]] = 0

    def remove_opponent_pair(self, idx:int):
        yx = self.current_coord
        #explicite coordinates of the stone to remove along each possible direction
        # from the stone just played
        stone_to_del = ((yx[0] + np.array([-2, -1]), yx[1] + np.array([0, 0])),
                        (yx[0] + np.array([1, 2]), yx[1] + np.array([0, 0])),
                        (yx[0] + np.array([0, 0]), yx[1] + np.array([-2, -1])),
                        (yx[0] + np.array([0, 0]), yx[1] + np.array([1, 2])),
                        (yx[0] + np.array([-2, -1]), yx[1] + np.array([-2, -1])),
                        (yx[0] + np.array([-2, -1]), yx[1] + np.array([1, 2])),
                        (yx[0] + np.array([1, 2]), yx[1] + np.array([-2, -1])),
                        (yx[0] + np.array([1, 2]), yx[1] + np.array([1, 2])))
        self.grid[stone_to_del[idx]] = 0


    def iscapture_position(self) -> bool:
        """[summary]
        Args:
            yx ([type]): [description]
            grid ([type]): [description]
        Returns:
            bool: [description]
        """
        global TOT
        yx = self.current_coord
        c = self.stone
        k_cap_line = c * np.array([[1, -1, -1, 1]])
        k_cap_diag = c * np.array([[1,  0,  0, 0],
                                   [0, -1,  0, 0],
                                   [0,  0, -1, 0],
                                   [0,  0,  0, 1]])
        extend_grid = np.zeros((SIZE + 6,SIZE + 6))
        extend_grid[3:-3, 3:-3] = self.grid
        extend_grid[yx[0] + 3, yx[1] + 3] = c
        
        print('>' * 5 + ' EXTENDED BOARD ')
        print(extend_grid[yx[0]:yx[0] + 4, yx[1] + 3:yx[1] + 4])
        r_conv_c1 = np.sum(np.multiply(extend_grid[yx[0]:yx[0] + 4, yx[1] + 3:yx[1] + 4], np.rot90(k_cap_line)))
        r_conv_c2 = np.sum(np.multiply(extend_grid[yx[0] + 3:yx[0] + 7, yx[1] + 3:yx[1] + 4], np.rot90(k_cap_line)))
        
        r_conv_l1 = np.sum(np.multiply(extend_grid[yx[0] + 3:yx[0]+4, yx[1]:yx[1] + 4], k_cap_line))
        r_conv_l2 = np.sum(np.multiply(extend_grid[yx[0] + 3:yx[0]+4, yx[1] + 3:yx[1] + 7], k_cap_line))
        
        r_conv_d1 = np.sum(np.multiply(extend_grid[yx[0]:yx[0] + 4, yx[1]:yx[1] + 4], k_cap_diag))
        r_conv_d2 = np.sum(np.multiply(extend_grid[yx[0]:yx[0] + 4, yx[1] + 3:yx[1] + 7], np.rot90(k_cap_diag)))
        r_conv_d3 = np.sum(np.multiply(extend_grid[yx[0] + 3:yx[0] + 7, yx[1]:yx[1] + 4], k_cap_diag))
        r_conv_d4 = np.sum(np.multiply(extend_grid[yx[0] + 3:yx[0] + 7, yx[1] + 3:yx[1] + 7], np.rot90(k_cap_diag)))
        res = [r_conv_c1, r_conv_c2, r_conv_l1, r_conv_l2, r_conv_d1, r_conv_d2, r_conv_d3, r_conv_d4]
        
        print(f' =================== {TOT} =================== ')
        TOT = TOT + 1
        for ii, r_conv in enumerate(res):
            print(f'({ii}) r_conv = {r_conv}')
            if (r_conv == 4):
                self.remove_opponent_pair(ii)
        print('\n')        
        if any([r == 4 for r in res]):
            return True
        return False


    @staticmethod
    def isbusy(xy, grid) -> bool:
        """[summary]
        Args:
            yx ([type]): [description]
            grid ([type]): [description]
        Returns:
            bool: [description]
        """
        if grid[xy[0]][xy[1]] != 0:
            return True
        return False

            
    @staticmethod
    def isdoublefreethree_position(yx, grid, color) -> bool:
        """[summary]
        Args:
            yx ([type]): [description]
            grid ([type]): [description]
        Returns:
            bool: [description]
        """
        tmp = np.zeros((SIZE + 8,SIZE + 8))
        tmp[yx[0] + 4, yx[1] + 4] = color
        tmp[4:-4, 4:-4] += color * grid + 1
        
        # Convolution sur la ligne 
        view_l = tmp[yx[0] + 4, yx[1]:yx[1] + 9]
        res_l = [np.sum(np.multiply(view_l[i:i+6], k_free_threes[0])) for i in range(4)]
        
        #Convolution sur la colonne:
        view_c = tmp[yx[0]:yx[0] + 9, yx[1] + 4]
        res_c = [np.sum(np.multiply(view_c[i:i+6], k_free_threes[1].flatten())) for i in range(4)]
        
        # Convolution sur diagonale descendante gauche-droite
        view_d1 = [tmp[yx[0]+i:yx[0]+6+i, yx[1]+i:yx[1]+6+i] for i in range(4)]
        res_d1 = [np.sum(np.multiply(view_d1[i], k_free_threes[2])) for i in range(4)]
        
        # Convolution sur diagonale montante gauche-droite
        view_d2 = [tmp[yx[0] +3 - i:yx[0] + 9 -i, yx[1]+i:yx[1]+6+i] for i in range(4)]
        res_d2 = [np.sum(np.multiply(view_d2[i], k_free_threes[3])) for i in range(4)]
        free_threes = 0
        if any([np.any(arr >= 16) for arr in res_l]):
            free_threes += 1
        if any([np.any(arr >= 16) for arr in res_c]):
            free_threes += 1
        if any([np.any(arr >= 16) for arr in res_d1]):
            free_threes += 1
        if any([np.any(arr >= 16) for arr in res_d2]):
            free_threes += 1
        if free_threes > 1:
            return True
        return False


    def isposition_available(self) -> bool:
        """Checks if the position for the stone the player wants
        to play is empty.
        Args:
        -----
            event (QtGui.QMouseEvent): Coordinates of mouse cursor
        Returns:
        --------
            (bool): boolean traducing if position is available.
        """
        if self.isbusy(self.current_coord, self.grid):
            print("position is not available.")
            return False
        if self.isdoublefreethree_position(self.current_coord, self.grid, self.stone):
            return False
        return True
        

    def placing_stone(self, event, color):
        """Creates and move and display the widget corresponding to the new
            stone (white/black) according to the coordinates in event (when
            clicking or when the algorithm is playing).
            The new stone is appended in the list of whitestone/blackstone
            widgets representing all the existing stones on the board.
        Args:
        -----
            event (QtGui.QMouseEvent): coordinates of mouse cursor.
            color (int): 1 == white and -1 == black
        """
        if isinstance(event, QtGui.QMouseEvent):
            nearest = nearest_coord(np.array([event.pos().x(), event.pos().y()]))
            coord = stone_to_board(nearest, self.stone, self.grid)
            self.grid[coord[0], coord[1]] = self.stone


    def UiGenBoard(self):
        """
        """
        self.coord_blackstones= np.argwhere(self.grid == BLACK)
        self.coord_whitestones = np.argwhere(self.grid == WHITE)
        
        for bs in self.coord_blackstones:
            stone = QLabel("", self.wdgts_UI3["board"])
            stone.setStyleSheet("background-color: transparent;")
            px_stone = QPixmap(assets["black_stone"]).scaled(26, 26, QtCore.Qt.KeepAspectRatio)
            stone.setPixmap(px_stone)
            xy = (31 * bs[::-1] + 6).astype('int32')
            stone.move(xy[0], xy[1])
            stone.show()
            self.W_blackstones.append(stone)

        for ws in self.coord_whitestones:
            stone = QLabel("", self.wdgts_UI3["board"])
            stone.setStyleSheet("background-color: transparent;")
            px_stone = QPixmap(assets["white_stone"]).scaled(26, 26, QtCore.Qt.KeepAspectRatio)
            stone.setPixmap(px_stone)
            xy = (31 * ws[::-1] + 6).astype('int32')
            stone.move(xy[0], xy[1])
            stone.show()
            self.W_whitestones.append(stone)


    def UiDestroyBoard(self):
        """
        """
        for ii in range(0, len(self.W_whitestones)):
            self.W_whitestones[ii].deleteLater()
        del(self.W_whitestones)
        
        for ii in range(0, len(self.W_blackstones)):
            self.W_blackstones[ii].deleteLater()
        del(self.W_blackstones)
        
        self.W_blackstones = []
        self.W_whitestones = []


    def mousePressEvent(self, event):
        def on_board(qpoint):
            """Checks if the position of the mouse click event is on the
                game board.
            Args:
            -----
                qpoint (QtCore.QPoint): coordinates in the plane of the cursor
            Returns:
            --------
                (bool): True if click is inside the board, False otherwise.y
            """
            x, y = qpoint.x(), qpoint.y()
            if (x >= 25) and (x <= 603) and (y >= 25) and (y <= 603):
                return True
            return False
        
        def iscurrentstate(history:History) -> bool:
            if history.i_current + 1 != history.tot_nodes:
                return False
            return True

        if (self.Stack.currentIndex() == 2) \
            and on_board(event.pos()) \
                and (event.buttons() == QtCore.Qt.LeftButton) \
                    and iscurrentstate(self.history):
            
            self.current_coord = current_coordinates(event.pos())
            if not self.isposition_available():
                return
            self.placing_stone(event, self.stone)
            self.iscapture_position()
            #self.check_board()
            self.i_round += 1
            self.UiDestroyBoard()
            self.UiGenBoard()

            self.node = Node(self.node, self.grid, color=-self.stone)
            self.history.add_nodes([self.node])
            self.stone = self.node.color

            self.node = self.agent.find_best_move(self.node)
            if self.node != None:
                self.history.add_nodes([self.node])
                prev_grid = self.grid
                self.grid = self.node.grid
                dgrid = prev_grid - self.grid

                self.UiDestroyBoard()
                self.UiGenBoard()
                self.i_round += 1
                self.stone *= -1