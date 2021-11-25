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
from game.history import History
import numpy as np
from numpy.lib.stride_tricks import as_strided


# =========================================================================== #
#                          | constants definition |                           #
# =========================================================================== #
#assets = {"button cancel": "assets/Cancel.png"}
dct_stylesheet ={"cancel_btn": "*{border: 0px solid '#FFCCCC';" +
                 "border-radius: 20px;" +
                 "font-size: 20px;" +
                 "color: white;" +
                 "padding: 0px 0px;" +
                 "margin: 0px 0px;}" +
                 "*:hover{background: '#FF6666';}"}

k_diags = np.array([0.25 * np.array([[-1, 0, 0, 0],
                                    [0, 1, 0, 0],
                                    [0, 0, 1, 0],
                                    [0, 0, 0, -1]]),
                    0.25 * np.array([[0, 0, 0, -1],
                                    [0, 0, 1, 0],
                                    [0, 1, 0, 0],
                                    [-1, 0, 0, 0]])])

k_lines = [0.25 * np.array([[-1, 1, 1, -1]]), 0.25 * np.array([[-1],[1],[1],[-1]])]

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
        self.grid = np.zeros((6,6), dtype=np.int8)
        self.W_whitestones = []
        self.W_blackstones = []

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
        if self.history.i_current < self.history.tot_nodes:
            self.history.i_current += 1
            self.grid = self.history.lst_nodes[self.history.i_current]
            self.UiDestroyBoard()
            self.UiGenBoard()

    def _subboard_4_Conv2D(self, k_shape:tuple, stride:tuple) -> np.array:
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
        view_shape = tuple(np.subtract(self.grid.shape, k_shape) + 1) + k_shape
        sub_grid = as_strided(self.grid, view_shape, stride * 2)
        return sub_grid


    def _my_conv2D(self, kernel:np.array) -> np.array:
        """ Retrieves the sub_grid from the function _subboard_4_Conv2D and performs
        the convolution (array multiplication + einstein sum along the 3rd and 4th
        dimensions).
        Args:
        -----
            * kernel ([np.array]): the kernel to use for convolution.
        """
        sub_grid = self._subboard_4_Conv2D(k_shape=kernel.shape, stride=self.grid.strides)
        res_conv = np.multiply(sub_grid, kernel)
        convolved = np.einsum('ijkl->ij', res_conv)
        return convolved.astype('int8')


    def check_board(self):
        """[summary]
        """
        ## Checking if white pair captured
        # Checking the diagonal:
        conv_diag1 = self._my_conv2D(k_diags[0])
        conv_diag2 = self._my_conv2D(k_diags[1])
        # Checking vertical and horizontal
        conv_lin1 = self._my_conv2D(k_lines[0])
        conv_lin2 = self._my_conv2D(k_lines[1])
        
        coord_cd1 = np.argwhere(conv_diag1 == 1)
        coord_cd2 = np.argwhere(conv_diag2 == 1)
        coord_cl1 = np.argwhere(conv_lin1 == 1)
        coord_cl2 = np.argwhere(conv_lin2 == 1)

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
        conv_diag1 = self._my_conv2D(-1 * k_diags[0])
        conv_diag2 = self._my_conv2D(-1 * k_diags[1])
        # Checking vertical and horizontal
        conv_lin1 = self._my_conv2D(-1 * k_lines[0])
        conv_lin2 = self._my_conv2D(-1 * k_lines[1])
        print(conv_lin1)
        print(conv_lin2)
        coord_cd1 = np.argwhere(conv_diag1 == 1)
        coord_cd2 = np.argwhere(conv_diag2 == 1)
        coord_cl1 = np.argwhere(conv_lin1 == 1)
        coord_cl2 = np.argwhere(conv_lin2 == 1)
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


    def remove_stone(self, idx, color):
        idx.reverse()
        if color == "white":
            for ii in idx:
                self.whitestone[ii][0].deleteLater()
                del(self.whitestone[ii])
        if color == "black":
            for ii in idx:
                self.blackstone[ii][0].deleteLater()
                del(self.blackstone[ii])


    def update_board(self, color:int):
        """ Update the board after the player/IA played.
        Update is called to remove stone which has been captured.
        Args:
        -----
            color (int): color of the last stone put on the board
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
        nearest = nearest_coord(np.array([event.pos().x(), event.pos().y()]))
        if self.grid[nearest[1] // 31 -1][nearest[0] // 31 -1] != 0:
            print("position is not available.")
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
                
    #def placing_stone(self, event, color):
    #    """Creates and move and display the widget corresponding to the new
    #        stone (white/black) according to the coordinates in event (when
    #        clicking or when the algorithm is playing).
    #        The new stone is appended in the list of whitestone/blackstone
    #        widgets representing all the existing stones on the board.
    #    Args:
    #    -----
    #        event (QtGui.QMouseEvent / np.array): we are interessed by the coordinates
    #        color (int): 1 == white and -1 == black
    #    """
    #    current_stone =  QLabel("", self.wdgts_UI3["board"])
    #    current_stone.setStyleSheet("background-color: transparent;")
    #    
    #    if color == 1: #white
    #        px_stone = QPixmap(assets["white_stone"])
    #    else:
    #        px_stone = QPixmap(assets["black_stone"])
    #    px_stone = px_stone.scaled(26, 26, QtCore.Qt.KeepAspectRatio)
    #    current_stone.setPixmap(px_stone)
    #    
    #    if isinstance(event, QtGui.QMouseEvent):
    #        nearest = nearest_coord(np.array([event.pos().x(), event.pos().y()]))
    #        coord = stone_to_board(nearest, self.stone, self.grid)
    #    else:
    #        nearest = nearest_coord(event)[::-1]
    #        coord = (event - 26) / 31
    #    if color == 1:
    #        self.whitestone.append((current_stone, coord.astype('int8')))
    #    else:
    #        self.blackstone.append((current_stone, coord.astype('int8')))
    #    
    #    current_stone.move(nearest[0] - 26, nearest[1] - 26)
    #    current_stone.show()


    def UiGenBoard(self):
        """
        """
        blackstones = np.argwhere(self.grid == -1)
        whitestones = np.argwhere(self.grid == 1)
        
        for coord in blackstones:
            stone = QLabel("", self.wdgts_UI3["board"])
            stone.setStyleSheet("background-color: transparent;")
            px_stone = QPixmap(assets["black_stone"]).scaled(26, 26, QtCore.Qt.KeepAspectRatio)
            stone.setPixmap(px_stone)
            self.W_whitestones.append((stone, coord))

        for coord in whitestones:
            stone = QLabel("", self.wdgts_UI3["board"])
            stone.setStyleSheet("background-color: transparent;")
            px_stone = QPixmap(assets["white_stone"]).scaled(26, 26, QtCore.Qt.KeepAspectRatio)
            stone.setPixmap(px_stone)
            self.W_whitestones.append((stone, coord))

        for wstone in self.W_whitestones:
            xy = (31 * wstone[1][::-1] + 6).astype('int32')
            wstone[0].move(xy[0], xy[1])
            wstone[0].show()
        for wstone in self.W_blackstones:
            xy = (31 * wstone[1][::-1] + 6).astype('int32')
            wstone[0].move(xy[0], xy[1])
            wstone[0].show()

    def UiDestroyBoard(self):
        """
        """
        for ii in range(0, len(self.W_whitestones)):
            self.W_whitestones[ii][0].deleteLater()
        del(self.W_whitestones)
        self.W_whitestones = []
        
        for ii in range(0, len(self.W_blackstones), -1):
            self.W_blackstones[ii][0].deleteLater()
        del(self.W_blackstones)
        self.W_blackstones = []


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

        if (self.Stack.currentIndex() == 2) and on_board(event.pos()) and (event.buttons() == QtCore.Qt.LeftButton):
            if not hasattr(self, 'grid'):
                self.grid = np.zeros((19,19))
            
            if not self.isposition_available(event):
                return
            self.placing_stone(event, self.stone)
            self.update_board(self.stone)
            self.UiDestroyBoard()
            self.UiGenBoard()
            #print("<><><> GRID Player  <><><>")
            #print(self.grid)
            #print("<><><> <><><><><><> <><><>")

            self.node = Node(self.node, self.grid, color=-self.stone)
            self.history.add_nodes([self.node])
            self.stone = self.node.color

            self.node = self.agent.find_best_move(self.node)
            #print("<><><>  GRID Agent  <><><>")
            #print(self.node.grid)
            #print("<><><> <><><><><><> <><><>")
            if self.node != None:
                self.history.add_nodes([self.node])
                prev_grid = self.grid
                self.grid = self.node.grid
                dgrid = prev_grid - self.grid

                self.UiDestroyBoard()
                self.UiGenBoard()
                self.stone *= -1

