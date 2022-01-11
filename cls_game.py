# =========================================================================== #
# ____________________  |Importation des lib/packages|   ____________________ #
# =========================================================================== #
from __future__ import annotations

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, \
    QVBoxLayout, QMessageBox, QGridLayout, QStackedWidget, QHBoxLayout, QVBoxLayout
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import QObject, QEvent, QRunnable, QThreadPool

from typing import Tuple, List
import numpy as np
from numpy.lib.stride_tricks import as_strided
from scipy.signal import convolve, convolve2d

from interface.game_interface import MyWindow, nearest_coord, stone_to_board, assets
from game.minimax import Solver
from game.board import Node, sum_kern3, sum_kern4
from game.history import History
from game.rules import iscapture_position, remove_opponent_pair


import time # TO REMOVE

# =========================================================================== #
#                          | constants definition |                           #
# =========================================================================== #
from constants import WHITE, BLACK, k_captures, k_freethree, TOP_LEFT_Y, TOP_LEFT_X, BOTTOM_RIGHT_X, BOTTOM_RIGHT_Y

TOT = 0

dct_stylesheet ={"cancel_btn": "*{border: 0px solid '#FFCCCC';" +
                 "border-radius: 20px;" +
                 "font-size: 20px;" +
                 "color: white;" +
                 "padding: 0px 0px;" +
                 "margin: 0px 0px;}" +
                 "*:hover{background: '#FF6666';}"}

SIZE = 19


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


def get_line_idx(yx:np.array):
    return (np.ones((1,9)) * yx[0]).astype('int8'), (np.arange(-4, 5) + yx[1]).astype('int8')


def get_col_idx(yx:np.array):
    return (np.arange(-4, 5) + yx[0]).astype('int8'), (np.ones((1,9)) * yx[1]).astype('int8')


def get_diag1_idx(yx:np.array):
    return (np.arange(-4, 5) + yx[0]).astype('int8'), (np.arange(-4, 5) + yx[1]).astype('int8')


def get_diag2_idx(yx:np.array):
    return (np.arange(4, -5, -1) + yx[0]).astype('int8'), (np.arange(-4, 5) + yx[1]).astype('int8')

# =========================================================================== #
#                           | Classes definition |                            #
# =========================================================================== #


class WorkerSignals(QObject):
    started = QtCore.pyqtSignal()
    finished = QtCore.pyqtSignal(int)
    timerswitching = QtCore.pyqtSignal(int)
    error = QtCore.pyqtSignal(tuple)
    result = QtCore.pyqtSignal(object)
    progress = QtCore.pyqtSignal(tuple)

class Worker(QRunnable):
    
    def __init__(self, node: Node, agent: Solver):
        super(Worker, self).__init__()
        self.node = node
        self.agent = agent
        self.signals = WorkerSignals()
        
    @QtCore.pyqtSlot()
    def run(self):
        node =self.agent.find_best_move(self.node)
        self.signals.result.emit(node)
        self.signals.finished.emit(node.color)
        self.signals.timerswitching.emit(-node.color)


class GameUI(MyWindow):
    
    timerSwitch = QtCore.pyqtSignal(int, int)
    timerReset = QtCore.pyqtSignal(int)
    timerStop = QtCore.pyqtSignal(int)
    timerStart = QtCore.pyqtSignal(int)
    boardGenerated = QtCore.pyqtSignal()
    boardDestroyed = QtCore.pyqtSignal()
    actionAgent = QtCore.pyqtSignal()
    freezeHuman = QtCore.pyqtSignal()
    unfreezeHuman = QtCore.pyqtSignal()
    scored = QtCore.pyqtSignal(tuple)
    gameEnd = QtCore.pyqtSignal(int)
    
    def __init__(self):
        super(GameUI, self).__init__()
        # Board creation and player related attributes
        self.p1_score = 0
        self.p2_score = 0

        # instance of Solver = generate the accessible moves from current node
        self.agent = Solver(depth=1)
        
        # Initialization of the tree.
        Node.metric = {BLACK: sum_kern3, WHITE: sum_kern3}
        self.node = Node(None, np.zeros((SIZE + 8,SIZE + 8), dtype=np.int8), WHITE)
        self.node.nb_free_three = 0

        self.i_round = 0
        self.history = History()
        self.history.add_nodes([self.node])
        
        # Connection of signals to the corresponding slots
        self.freeze = False
        self.freezeHuman.connect(self.freeze_human_agent)
        self.unfreezeHuman.connect(self.unfreeze_human_agent)
        self.timerSwitch.connect(self._timer_switch)
        self.timerReset.connect(self._timer_reset)
        self.timerStart.connect(self._timer_start)
        self.timerStop.connect(self._timer_stop)
        self.boardGenerated.connect(self.UiGenBoard)
        self.boardDestroyed.connect(self.UiDestroyBoard)
        self.scored.connect(self.game_score)
        self.gameEnd.connect(self.game_end)
        self.actionAgent.connect(self.agent_exec_move)
        self.threadpool = QThreadPool()


    def game_quit(self):
        super().game_quit()
        self.p1_score = 0
        self.p2_score = 0
        self.node = Node(None, np.zeros((SIZE + 8,SIZE + 8), dtype=np.int8), WHITE)
        self.node.nb_free_three = 0

        self.i_round = 0
        self.history = History()
        self.history.add_nodes([self.node])
        
        self.agent = Solver(depth=1)


    def game_play(self):
        super().game_play()
        self.timerStart.emit(self.stone) # starting the timer of the 1st player as soon the game scene is displayed


    def game_backward(self):
        """[summary]
        """
        if self.history.i_current > 0:
            self.freeze = True
            self.history.i_current -= 1
            #self.grid = self.history.lst_nodes[self.history.i_current]
            self.boardDestroyed.emit()


    def game_forward(self):
        """[summary]
        """
        if self.history.i_current + 1 < self.history.tot_nodes:
            self.history.i_current += 1
            #self.grid = self.history.lst_nodes[self.history.i_current]
            self.boardDestroyed.emit()
        
        if self.history.i_current == self.history.tot_nodes:
            self.freeze = False

    @QtCore.pyqtSlot(tuple)
    def game_score(self, scores: Tuple[int]):
        """[summary]
        """
        self.p1_score += scores[0]
        self.p2_score += scores[1]
        self.wdgts_UI3["score p1"].setPixmap(QPixmap(assets[f"img_{self.p1_score}"]))
        self.wdgts_UI3["score p2"].setPixmap(QPixmap(assets[f"img_{self.p2_score}"]))
        
        if (self.p1_score == 5) or (self.player_2 == 5):
            self.gameEnd.emit(self.node.color)

    @QtCore.pyqtSlot(int)
    def game_end(self, color:int):
        if color == BLACK:
            player = 1
        else:
            player = 2
        #self.qmessage = 
        QMessageBox.information("End of Game", f"Player {player} won!")
        
        

    @staticmethod
    def _DEPRECATED_subboard_4_Conv2D(grid, k_shape:tuple, stride:tuple) -> np.array:
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
    def _DEPRECATED_my_conv2D(grid, kernel:np.array) -> np.array:
        """ Retrieves the sub_grid from the function _subboard_4_Conv2D and performs
        the convolution (array multiplication + einstein sum along the 3rd and 4th
        dimensions).
        Args:
        -----
            * kernel ([np.array]): the kernel to use for convolution.
        """
        sub_grid = GameUI._subboard_4_Conv2D(grid, k_shape=kernel.shape, stride=grid.strides)
        res_conv = np.dot(sub_grid, kernel)
        print("sub_grid = \n", sub_grid)
        print("res_conv = \n", res_conv)
        convolved = np.einsum('ijkl->ij', res_conv)
        return convolved


    @staticmethod
    def isbusy(xy, grid) -> bool:
        """ Verifies if the position xy on the board is occupied by a stone
        Args:
        -----
            yx (np.array([int, int])): coordinates to check.
            grid (np.array[int (19 x 19)]): Go board
        Returns:
        --------
            bool: True if position on board is occupied.
                  False if not.
        """
        if grid[xy[0]][xy[1]] != 0:
            return True
        return False

            
    @staticmethod
    def isdoublefreethree_position(yx:np.array, grid:np.array, color:int) -> bool:
        """ Verifies if the position yx on board is a double free three position.
        A double free three is a position leading to the creation of 2 simultaneous free three.
        Args:
        -----
            yx (np.array([int, int])): coordinates to check.
            grid (np.array[int (19 x 19)]): Go board
            color (int): either 1 or -1.
        Returns:
        --------
            bool: True if position on board is occupied.
                  False if not.
        """
        pad_width = 5
        c = color
        extend_grid = np.pad(grid + c, pad_width, "constant", constant_values = (0))
        extend_grid[yx[0] + pad_width, yx[1] + pad_width] = 2 * c
        res = []
        res.append(np.convolve(extend_grid[get_line_idx(yx + pad_width)].reshape(-1,), c * k_freethree, "valid"))
        res.append(np.convolve(extend_grid[get_col_idx(yx + pad_width)].reshape(-1,), c * k_freethree, "valid"))
        res.append(np.convolve(extend_grid[get_diag1_idx(yx + pad_width)], c * k_freethree, "valid"))
        res.append(np.convolve(extend_grid[get_diag2_idx(yx + pad_width)], c * k_freethree, "valid"))
        nb_free_three = 0
        for r_conv in res:
            if (r_conv >= 16).any():
                nb_free_three += 1
        if nb_free_three > 1:
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
        if self.isbusy(self.current_coord, self.node.grid[4:-4, 4:-4]):
            print("position is not available.")
            return False
        if self.isdoublefreethree_position(self.current_coord, self.node.grid[4 : -4, 4 : -4], self.stone):
            print("position is not available: double free three not allows.")
            return False
        return True
        

    def create_node(self):
        """Creates a new node based on the position on board where player clicked.
        """
        # retrieving the grid of the parent node
        grid = np.copy(self.node.grid)
        
        # Updating the new grid: placing stone and checking if there are captures.
        grid[self.current_coord[0] + 4, self.current_coord[1] + 4] = self.stone
        # Child node creation
        node = Node(self.node, grid, self.stone, self.current_coord + 4)

        return node

    @QtCore.pyqtSlot()
    def UiGenBoard(self):
        """
        """
        #self.coord_blackstones = np.argwhere(self.node.grid[4 : -4, 4 : -4] == BLACK)
        #self.coord_whitestones = np.argwhere(self.node.grid[4 : -4, 4 : -4] == WHITE)
        self.coord_blackstones = np.argwhere(self.history.lst_nodes[self.history.i_current][4 : -4, 4 : -4] == BLACK)
        self.coord_whitestones = np.argwhere(self.history.lst_nodes[self.history.i_current][4 : -4, 4 : -4] == WHITE)
        
        
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
        if self.node.captured_pairs > 0:
            if self.node.color == BLACK:
                self.scored.emit((self.node.captured_pairs, 0))
            else:
                self.scored.emit((0, self.node.captured_pairs))


    @QtCore.pyqtSlot()
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
        self.boardGenerated.emit()

    @QtCore.pyqtSlot(int)
    def _timer_start(self, color:int):
        if color is BLACK:
            self.start_black = True
        if color is WHITE:
            self.start_white = True


    @QtCore.pyqtSlot(int)
    def _timer_stop(self, color:int):
        if color is BLACK:
            self.start_black = False
        if color is WHITE:
            self.start_white = False


    @QtCore.pyqtSlot(int, int)
    def _timer_switch(self, to_stop: int, to_start: int):
        self.timerstop.emit(to_stop)
        self.timerstart.emit(to_start)


    @QtCore.pyqtSlot(int)
    def _timer_reset(self, color: int):
        if color == BLACK:
            self.wdgts_UI3[f"display timer 1"].setText("  00.00 s")
            self.count_black = 0
        if color == WHITE:
           self.wdgts_UI3[f"display timer 2"].setText("  00.00 s")
           self.count_white = 0

    @QtCore.pyqtSlot(Node)
    def _catch_node_(self, node):
        self.node = node
        self.history.add_nodes([self.node])
        

    @QtCore.pyqtSlot()
    def agent_exec_move(self):
        #self.node = self.agent.find_best_move(self.node)
        worker = Worker(self.node, self.agent)
        worker.signals.result.connect(self._catch_node_)
        worker.signals.finished.connect(self.UiDestroyBoard)
        worker.signals.finished.connect(self._timer_stop)
        worker.signals.finished.connect(self.unfreeze_human_agent)
        
        worker.signals.timerswitching.connect(self._timer_reset)
        worker.signals.timerswitching.connect(self._timer_start)
        self.threadpool.start(worker)
        
        if self.node != None:
            self.history.add_nodes([self.node])
            # Changing self.stone color and incrementing round_counter
            self.stone = -self.stone
            self.i_round += 1
            #self.boardDestroyed.emit()


    @QtCore.pyqtSlot()
    def freeze_human_agent(self):
        self.freeze = True


    @QtCore.pyqtSlot()
    def unfreeze_human_agent(self):
        self.freeze = False


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
            if (x >= TOP_LEFT_X) and (x <= BOTTOM_RIGHT_X) \
                and (y >= TOP_LEFT_Y) and (y <= BOTTOM_RIGHT_Y):
                return True
            return False
        
        def iscurrentstate(history:History) -> bool:
            if history.i_current + 1 != history.tot_nodes:
                return False
            return True

        if self.freeze:
            return
        self.freezeHuman.emit()

        if (self.Stack.currentIndex() == 2) \
            and on_board(event.pos()) \
                and (event.buttons() == QtCore.Qt.LeftButton) \
                    and iscurrentstate(self.history):
            
            self.current_coord = current_coordinates(event.pos())
            if not self.isposition_available():
                self.unfreezeHuman.emit()
                return
            
            self.timerStop.emit(self.stone)

            self.node = self.create_node()
            self.history.add_nodes([self.node])
            self.boardDestroyed.emit()

            # Changing self.stone color and incrementing round_counter
            self.i_round += 1
            self.stone = -self.stone
            
            self.timerReset.emit(self.stone)
            self.timerStart.emit(self.stone)
            if self.p2_type == "IA":
                self.actionAgent.emit()
        
        self.unfreezeHuman.emit()