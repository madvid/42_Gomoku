# =========================================================================== #
# ____________________  |Importation des lib/packages|   ____________________ #
# =========================================================================== #
from __future__ import annotations

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, \
    QVBoxLayout, QWidget, QGridLayout, QStackedWidget, QHBoxLayout, QVBoxLayout
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QCursor

from typing import Tuple
import numpy as np
from numpy.lib.stride_tricks import as_strided

from interface.game_interface import MyWindow, nearest_coord, stone_to_board, assets
from game.minimax import Solver
from game.board import Node
from game.history import History


# =========================================================================== #
#                          | constants definition |                           #
# =========================================================================== #

BLACK = 1
WHITE = -1

dct_stylesheet ={"cancel_btn": "*{border: 0px solid '#FFCCCC';" +
                 "border-radius: 20px;" +
                 "font-size: 20px;" +
                 "color: white;" +
                 "padding: 0px 0px;" +
                 "margin: 0px 0px;}" +
                 "*:hover{background: '#FF6666';}"}

k_diags = np.array([np.array([[BLACK, 0,     0,     0],
                              [0,     WHITE, 0,     0],
                              [0,     0,     WHITE, 0],
                              [0,     0,     0,     BLACK]]),
                    np.array([[0,     0,     0,     BLACK],
                              [0,     0,     WHITE, 0],
                              [0,     WHITE, 0,     0],
                              [BLACK, 0,     0,     0]])])

k_lines = [np.array([[BLACK, WHITE, WHITE, BLACK]]),
           np.array([[BLACK],
                     [WHITE],
                     [WHITE],
                     [BLACK]])]

k_capture_l = np.array([[BLACK],[WHITE],[0],[BLACK]])
k_capture_d = np.array([[BLACK, 0,     0, 0],
                        [0,     WHITE, 0, 0],
                        [0,     0,     0, 0],
                        [0,     0,     0, BLACK]])

k_captures = [k_capture_l, np.rot90(k_capture_l), np.rot90(k_capture_l, k=2), np.rot90(k_capture_l, k=3),
              -k_capture_l, np.rot90(-k_capture_l), -np.rot90(k_capture_l, k=2), -np.rot90(k_capture_l, k=3),
              k_capture_d, np.rot90(k_capture_d), np.rot90(k_capture_d, k=2), np.rot90(k_capture_d, k=3),
              -k_capture_d, np.rot90(-k_capture_d), -np.rot90(k_capture_d, k=2), -np.rot90(k_capture_d, k=3)]

k_freethree_l = np.array([[1, 2, 2, 2, 2, 1]])
k_freethree_d = np.array([[1, 0, 0, 0, 0, 0],
                          [0, 2, 0, 0, 0, 0],
                          [0, 0, 2, 0, 0, 0],
                          [0, 0, 0, 2, 0, 0],
                          [0, 0, 0, 0, 2, 0],
                          [0, 0, 0, 0, 0, 1]])
k_free_threes = [k_freethree_l, np.rot90(k_freethree_l), k_freethree_d, np.rot90(k_freethree_d)]


# =========================================================================== #
#                          | fonctions definition |                           #
# =========================================================================== #


# =========================================================================== #
#                           | Classes definition |                            #
# =========================================================================== #
class GameUI(MyWindow):
    def __init__(self, gmode:int):
        super(GameUI, self).__init__()
        # Board creation and player related attributes
        self.grid = np.zeros((6,6), dtype=np.int8)
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
        conv_diag1 = GameUI._my_conv2D(k_diags[0])
        conv_diag2 = GameUI._my_conv2D(k_diags[1])
        # Checking vertical and horizontal
        conv_lin1 = GameUI._my_conv2D(k_lines[0])
        conv_lin2 = GameUI._my_conv2D(k_lines[1])
        
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
        conv_diag1 = GameUI._my_conv2D(-1 * k_diags[0])
        conv_diag2 = GameUI._my_conv2D(-1 * k_diags[1])
        # Checking vertical and horizontal
        conv_lin1 = GameUI._my_conv2D(-1 * k_lines[0])
        conv_lin2 = GameUI._my_conv2D(-1 * k_lines[1])

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


    def isposition_available(self, event) -> bool:
        """Checks if the position for the stone the player wants
        to play is empty.
        Args:
        -----
            event (QtGui.QMouseEvent): Coordinates of mouse cursor
        Returns:
        --------
            (bool): boolean traducing if position is available.
        """
        extend_grid = np.zeros((23,23))
        extend_grid[2:-2][2:-2] = self.grid
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
            
        def iscapture_position(yx, grid) -> bool:
            """[summary]

            Args:
                yx ([type]): [description]
                grid ([type]): [description]

            Returns:
                bool: [description]
            """
            r_start, r_end = yx[0] - 2, yx[0] + 2
            c_start, c_end = yx[1] - 2, yx[1] + 2
            res = [GameUI._my_conv2D(grid[r_start:r_end][c_start:c_end], kernel) for kernel in k_captures]

            if any([np.any(arr == 3) for arr in res]):
                return True
            return False

        def issimplefreethree_position(yx, grid):
            """[summary]

            Args:
                yx ([type]): [description]
                grid ([type]): [description]

            Returns:
                ___: [description]
            """
            tmp = np.zeros((27,27))
            tmp[4:-4, 4:-4] = grid + 1 
            # Verifier si c'est la bonne fenetre, centrée sur la position ou la stone
            # va etre placé !!!
            #r_start, r_end = yx[0] - 4, yx[0] + 4
            #c_start, c_end = yx[1] - 4, yx[1] + 4
            r_start, r_end = yx[0], yx[0] + 8
            c_start, c_end = yx[1], yx[1] + 8
            res = [GameUI._my_conv2D(grid[r_start:r_end, c_start:c_end], kernel) for kernel in k_free_threes]
            
            if any([np.any(arr == 15) for arr in res]):
                return True
            return False
            
        def isdoublefreethree_position(yx, grid) -> bool:
            """[summary]

            Args:
                yx ([type]): [description]
                grid ([type]): [description]

            Returns:
                bool: [description]
            """
            if condition:
                return True
            return False
        
        nearest = nearest_coord(np.array([event.pos().x(), event.pos().y()]))
        if isbusy(nearest[::-1] // 31 - 1, self.grid):
            print("position is not available.")
            return False
        if iscapture_position(nearest[::-1] // 31 - 1, extend_grid):
            return False
        if isdoublefreethree_position(nearest[::-1] // 31 - 1, extend_grid):
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
            
            if not self.isposition_available(event):
                return
            self.placing_stone(event, self.stone)
            self.check_board()
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