# =========================================================================== #
# ____________________  |Importation des lib/packages|   ____________________ #
# =========================================================================== #
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, \
    QVBoxLayout, QWidget, QGridLayout, QStackedWidget, QHBoxLayout, QVBoxLayout
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import QTimer
import numpy as np
import numpy.typing as npt
from math import fabs
from typing import Tuple

# =========================================================================== #
# ___________________________    |CONSTANTES|    ____________________________ #
# =========================================================================== #
from constants import TOP_LEFT_X, TOP_LEFT_Y, BOTTOM_RIGHT_X, BOTTOM_RIGHT_Y


BLACK = 1
WHITE = -1

W_WIDTH = 1080
W_HEIGHT = 940
MAIN_BTN_WIDTH = int(0.15 * W_WIDTH)
MAIN_BTN_HEIGHT = int(0.8 * W_HEIGHT)

WIDGETS_WH = {"stack1_logo": [int(W_WIDTH), int(0.4 * W_HEIGHT)],
              "button pvp": [int(0.8 * W_WIDTH), int(0.15 * W_HEIGHT)],
              "button pva": [int(0.8 * W_WIDTH), int(0.15 * W_HEIGHT)],
              "stack2_logo": [int(W_WIDTH), int(W_HEIGHT / 6.)],
              "wdgt_character": [int(0.32 * W_HEIGHT), int(0.32 * W_HEIGHT)],
                "img_character": [int(0.28 * W_HEIGHT), int(0.28 * W_HEIGHT)],
              "stack2_back": [int(W_WIDTH / 6.), int(W_HEIGHT / 6.)],
              "stack2_play": [int(W_WIDTH / 6.), int(W_HEIGHT / 6.)],
              "stack3_board": [int(4. * W_WIDTH / 6.), int(4. * W_HEIGHT / 6.)],
              "stack3_player": [int(2. * W_WIDTH / 6.), int(W_HEIGHT / 6.)],
              "stack3_lscore": [int(W_WIDTH / 6.), int(W_HEIGHT / 6.)],
              "stack3_score": [int(W_WIDTH / 6.), int(W_HEIGHT / 6.)],
              "stack3_quit": [int(2. * W_WIDTH / 6.), int(W_HEIGHT / 6.)]}

CHARACTERS = {"character 1":{"name":"Elon Musk", "file":"assets/pixel_elon.png", "check": False},
              "character 2":{"name":"Lee Sedol", "file":"assets/pixel_lee_sedol.png", "check": False},
              "character 3":{"name":"Sophie Viger", "file":"assets/pixel_sophie.png", "check": False},
              "character 4":{"name":"Matthieu David", "file":"assets/pixel_mdavid.png", "check": False},
              "character 5":{"name":"Pierre Peigne", "file":"assets/pixel_ppeigne.png", "check": False},
              "character 6":{"name":"Richard Feynman", "file":"assets/pixel_feynman.png", "check": False},}

assets = {"button back": "assets/BACK.png",
          "button play": "assets/PLAY.png",
          "button pva": "assets/Player_vs_IA.png",
          "button pvp": "assets/Player_vs_Player.png",
          "button quit": "assets/QUIT.png",
          "button backward": "assets/BACKWARD.png",
          "button forward": "assets/FORWARD.png",
          "img_0": "assets/0.png",
          "img_1": "assets/1.png",
          "img_2": "assets/2.png",
          "img_3": "assets/3.png",
          "img_4": "assets/4.png",
          "img_5": "assets/5.png",
          "img_board": "assets/board.png",
          "img_chrct_select": "assets/character_selection.png",
          "img_gomoku": "assets/Gomoku.png",
          "img_player1": "assets/Player1.png",
          "img_player2": "assets/Player2.png",
          "img_score": "assets/Pairs.png",
          "chr_Elon": "assets/pixel_elon.png",
          "chr_Feynman": "assets/pixel_feynman.png",
          "chr_Lee_Sedol": "assets/pixel_lee_sedol.png",
          "chr_Sophie": "assets/pixel_sophie.png",
          "chr_Mdavid": "assets/pixel_mdavid.png",
          "chr_Ppeigne": "assets/pixel_ppeigne.png",
          "white_stone": "assets/stone_white.png",
          "black_stone": "assets/stone_black.png",
          "timer": "assets/time.png"
          }

dct_stylesheet = {"menu_button": "*{border: 4px solid '#1B5DBF';" +
                                 "border-radius: 35px;" +
                                 "font-size: 15px;" +
                                 "color: white;" +
                                 "padding: 25px 0px;" +
                                 "margin: 0px 0px;}" +
                                 "*:hover{background: '#0067FF';}",
                "character": "*{border: 4px solid '#FFFFFF';" +
                                 "border-radius: 0px;" +
                                 "font-size: 20px;" +
                                 "color: white;" +
                                 "padding: 5px;" +
                                 "margin: 0px;}" +
                                 "*:hover{background: '#00CC00';}",
                 "play_btn": "*{border: 0px solid '#1B5DBF';" +
                                "border-radius: 20px;" +
                                "font-size: 20px;" +
                                "color: white;" +
                                "padding: 0px 0px;" +
                                "margin: 0px 0px;}" +
                                "*:hover{background: 'green';}",
                 "back_btn": "*{border: 0px solid '#1B5DBF';" +
                                "border-radius: 20px;" +
                                "font-size: 20px;" +
                                "color: white;" +
                                "padding: 0px 0px;" +
                                "margin: 0px 0px;}" +
                                "*:hover{background: 'red';}",
                 "quit_btn": "*{border: 0px solid '#1B5DBF';" +
                                "border-radius: 20px;" +
                                "font-size: 20px;" +
                                "color: white;" +
                                "padding: 0px 0px;" +
                                "margin: 0px 0px;}" +
                                "*:hover{background: 'red';}",
                 "backwrd_btn": "*{background: '#0B3D6F';" +
                                "border-radius: 20px;" +
                                "font-size: 20px;" +
                                "color: white;" +
                                "padding: 0px 0px;" +
                                "margin: 0px 0px;}" +
                                "*:hover{background: '#33B8FF';}",
                 "forwrd_btn": "*{background: '#48BCD7';" +
                                "border-radius: 20px;" +
                                "font-size: 20px;" +
                                "color: white;" +
                                "padding: 0px 0px;" +
                                "margin: 0px 0px;}" +
                                "*:hover{background: '#ABE1ED';}"}

nodes_x , nodes_y = 31 * np.arange(1, 20), 31 * np.arange(1, 20)
coords = np.array(np.meshgrid(nodes_x, nodes_y)).T.reshape(-1,2)

# =========================================================================== #
# ___________________________    |FUNCTIONS|     ____________________________ #
# =========================================================================== #

def nearest_coord(point:np.array) -> np.array:
    trsl_pt = point - np.array([TOP_LEFT_X, TOP_LEFT_Y])
    ii = trsl_pt[0] // 31
    jj = trsl_pt[1] // 31
    if fabs(trsl_pt[0] - ii * 31) >  fabs(trsl_pt[0] - (ii + 1) * 31):
        ii += 1
    if fabs(trsl_pt[1] - jj * 31) >  fabs(trsl_pt[1] - (jj + 1) * 31):
        jj += 1
    return np.array([ii * 31, jj * 31]) 


def stone_to_board(coord:Tuple[int, int], color:int, grid:np.array):
    arr_idx = np.array([(coord[1] // 31) - 1, (coord[0] // 31) - 1])
    grid[arr_idx[0], arr_idx[1]] = color
    return arr_idx


# =========================================================================== #
# ___________________________     |CLASSES|      ____________________________ #
# =========================================================================== #

class MyWindow(QWidget):

    def __init__(self):
        super(MyWindow, self).__init__()
        # Parameters of the window
        self.setWindowTitle("Gomoku by mdavid & ppeigne")
        self.setFixedSize(W_WIDTH, W_HEIGHT)
        self.setStyleSheet("background: #152338;")

        # Widgets which matter for the update of the board (np.array)
        self.stone = BLACK # 1 is black and -1 is white
        self.W_whitestones = []
        self.W_blackstones = []
        self.coord_whitestones = []
        self.coord_blackstones = []

        # Related to character selection on screen 2
        self.player_1 = None
        self.player_2 = None
        self.p1_type = None
        self.p2_type = None
        
        # Multi screen in the window related widget
        self.stack1 = QWidget(self)
        self.stack2 = QWidget(self)
        self.stack3 = QWidget(self)
        self.stack1UI()
        self.stack2UI()
        self.stack3UI()
        self.Stack = QStackedWidget(self)
        self.Stack.addWidget(self.stack1)
        self.Stack.addWidget(self.stack2)
        self.Stack.addWidget(self.stack3)
        
        # Timer related
        self.count_black = 0
        self.count_white = 0
        self.start_black = False
        self.start_white = False


    def stack1UI(self):
        # -------- MAIN MENU FRAME -------- #
        # Label (logo) widget
        image_main = QPixmap(assets["img_gomoku"])
        self.wdgts_UI1 = {"header": QLabel(),
                          "button pvp": QPushButton("", self.stack1),
                          "button pva": QPushButton("", self.stack1)
                          }
        
        self.wdgts_UI1["header"].setPixmap(image_main)
        self.wdgts_UI1["header"].setAlignment(QtCore.Qt.AlignCenter)
        self.wdgts_UI1["header"].setStyleSheet("margin-top: 0px;")
        self.wdgts_UI1["header"].resize(*WIDGETS_WH["stack1_logo"])

        # Button widgets
        for key in ["button pvp", "button pva"]:
            self.wdgts_UI1[key].setStyleSheet(dct_stylesheet["menu_button"])
            self.wdgts_UI1[key].setIcon(QtGui.QIcon(assets[key]))
            self.wdgts_UI1[key].setIconSize(QtCore.QSize(640,50))
            self.wdgts_UI1[key].resize(*WIDGETS_WH[key])
            self.wdgts_UI1[key].setCursor(QCursor(QtCore.Qt.PointingHandCursor))

        # Connecting button signals to corresponding slots
        self.wdgts_UI1["button pvp"].clicked.connect(self.game_pvp)
        self.wdgts_UI1["button pva"].clicked.connect(self.game_pva)

        # Placing menu widgets in vertical layout:
        vlayout = QVBoxLayout()
        for wdgt, strech in zip(self.wdgts_UI1.values(), [1,2,0]):
            vlayout.addStretch(strech)
            vlayout.addWidget(wdgt)
        vlayout.addStretch(1)

        # Placing the vertical layout into a horizontal layout (centering ?)
        layout = QHBoxLayout()
        layout.addStretch(1)
        layout.addLayout(vlayout)
        layout.addStretch(1)
        self.stack1.setLayout(layout)
        self.stack1.setLayout(vlayout)
        

    def stack2UI(self):
        # -------- SELECT PERSO FRAME -------- #
        self.wdgts_UI2 = {"header": QLabel(),
                          "character 1": QPushButton("", self.stack2),
                          "character 2": QPushButton("", self.stack2),
                          "character 3": QPushButton("", self.stack2),
                          "character 4": QPushButton("", self.stack2),
                          "character 5": QPushButton("", self.stack2),
                          "character 6": QPushButton("", self.stack2),
                          "button play": QPushButton("", self.stack2),
                          "button back": QPushButton("", self.stack2)
                          }
        # Display logo
        image_select = QPixmap("assets/character_selection.png")
        self.wdgts_UI2["header"].setPixmap(image_select)
        self.wdgts_UI2["header"].setAlignment(QtCore.Qt.AlignCenter)
        self.wdgts_UI2["header"].setStyleSheet("margin-top: 0px;")
        self.wdgts_UI2["header"].setFixedSize(QtCore.QSize(*WIDGETS_WH["stack2_logo"]))

        for ii in range(1,7):
            self.wdgts_UI2[f"character {ii}"].setIcon(QtGui.QIcon(CHARACTERS[f"character {ii}"]["file"]))
            self.wdgts_UI2[f"character {ii}"].setIconSize(QtCore.QSize(*WIDGETS_WH["img_character"]))
            self.wdgts_UI2[f"character {ii}"].setCursor(QCursor(QtCore.Qt.PointingHandCursor))
            self.wdgts_UI2[f"character {ii}"].setStyleSheet(dct_stylesheet["character"])
            self.wdgts_UI2[f"character {ii}"].setFixedSize(QtCore.QSize(*WIDGETS_WH["wdgt_character"]))

        
        for key, fname in zip(["play", "back"], ["PLAY", "BACK"]):
            self.wdgts_UI2[f"button {key}"].setIcon(QtGui.QIcon(f'assets/{fname}.png'))
            self.wdgts_UI2[f"button {key}"].setIconSize(QtCore.QSize(203,67))
            self.wdgts_UI2[f"button {key}"].setStyleSheet(dct_stylesheet[f"{key}_btn"])
            self.wdgts_UI2[f"button {key}"].setFixedSize(210, 70)
        

        # Placing all the widgets in the select character frame:
        grid = QGridLayout()
        grid.addWidget(self.wdgts_UI2["header"], 0, 0, 1, 6, alignment=QtCore.Qt.AlignCenter)
        grid.addWidget(self.wdgts_UI2["character 1"], 1, 0, 2, 2, alignment=QtCore.Qt.AlignRight)
        grid.addWidget(self.wdgts_UI2["character 2"], 1, 2, 2, 2, alignment=QtCore.Qt.AlignCenter)
        grid.addWidget(self.wdgts_UI2["character 3"], 1, 4, 2, 2, alignment=QtCore.Qt.AlignLeft)
        grid.addWidget(self.wdgts_UI2["character 4"], 3, 0, 2, 2, alignment=QtCore.Qt.AlignRight)
        grid.addWidget(self.wdgts_UI2["character 5"], 3, 2, 2, 2, alignment=QtCore.Qt.AlignCenter)
        grid.addWidget(self.wdgts_UI2["character 6"], 3, 4, 2, 2, alignment=QtCore.Qt.AlignLeft)
        grid.addWidget(self.wdgts_UI2["button play"], 5, 4, 1, 2, alignment=QtCore.Qt.AlignCenter)
        grid.addWidget(self.wdgts_UI2["button back"], 5, 0, 1, 2, alignment=QtCore.Qt.AlignCenter)


        self.wdgts_UI2["character 1"].clicked.connect(self.select_character_1)
        self.wdgts_UI2["character 2"].clicked.connect(self.select_character_2)
        self.wdgts_UI2["character 3"].clicked.connect(self.select_character_3)
        self.wdgts_UI2["character 4"].clicked.connect(self.select_character_4)
        self.wdgts_UI2["character 5"].clicked.connect(self.select_character_5)
        self.wdgts_UI2["character 6"].clicked.connect(self.select_character_6)
        self.wdgts_UI2["button play"].clicked.connect(self.game_play)
        self.wdgts_UI2["button back"].clicked.connect(self.game_back)

        self.stack2.setLayout(grid)


    def stack3UI(self):
        # -------- GAME FRAME -------- #
        self.wdgts_UI3 = {"board": QLabel(self.stack3),
                          "label p1": QLabel(self.stack3),
                          "label p2": QLabel(self.stack3),
                          "label score p1": QLabel(self.stack3),
                          "label score p2": QLabel(self.stack3),
                          "score p1": QLabel(self.stack3),
                          "score p2": QLabel(self.stack3),
                          "button quit": QPushButton("",self.stack3),
                          "button backward": QPushButton("",self.stack3),
                          "button forward": QPushButton("",self.stack3),
                          "label timer 1": QLabel(self.stack3),
                          "label timer 2": QLabel(self.stack3),
                          "display timer 1": QLabel("  00.00 s", self.stack3),
                          "display timer 2": QLabel("  00.00 s", self.stack3),
                          "timer 1": QTimer(self.stack3),
                          "timer 2": QTimer(self.stack3),
                          }
        # Display logo
        img_board = QPixmap(assets["img_board"])
        img_board = img_board.scaled(606, 606)
        self.wdgts_UI3["board"].setPixmap(img_board)

        self.wdgts_UI3["label p1"].setPixmap(QPixmap(assets["img_player1"]))
        self.wdgts_UI3["label p2"].setPixmap(QPixmap(assets["img_player2"]))
        self.wdgts_UI3["label score p1"].setPixmap(QPixmap(assets["img_score"]))
        self.wdgts_UI3["label score p2"].setPixmap(QPixmap(assets["img_score"]))
        self.wdgts_UI3["score p1"].setPixmap(QPixmap(assets["img_0"]))
        self.wdgts_UI3["score p2"].setPixmap(QPixmap(assets["img_0"]))

        self.wdgts_UI3["button quit"].setIcon(QtGui.QIcon(assets["button quit"]))
        self.wdgts_UI3["button quit"].setIconSize(QtCore.QSize(203,67))
        self.wdgts_UI3["button quit"].setStyleSheet(dct_stylesheet["back_btn"])
        self.wdgts_UI3["button quit"].clicked.connect(self.game_quit)

        self.wdgts_UI3["button backward"].setIcon(QtGui.QIcon(assets["button backward"]))
        self.wdgts_UI3["button backward"].setIconSize(QtCore.QSize(203,67))
        self.wdgts_UI3["button backward"].setStyleSheet(dct_stylesheet["backwrd_btn"])
        self.wdgts_UI3["button backward"].clicked.connect(self.game_backward)

        self.wdgts_UI3["button forward"].setIcon(QtGui.QIcon(assets["button forward"]))
        self.wdgts_UI3["button forward"].setIconSize(QtCore.QSize(203,67))
        self.wdgts_UI3["button forward"].setStyleSheet(dct_stylesheet["forwrd_btn"])
        self.wdgts_UI3["button forward"].clicked.connect(self.game_forward)

        self.wdgts_UI3["label timer 1"].setPixmap(QPixmap(assets["timer"]))
        self.wdgts_UI3["label timer 2"].setPixmap(QPixmap(assets["timer"]))
        self.wdgts_UI3["display timer 1"].setStyleSheet("*{font-size: 24px; color: White;}")
        self.wdgts_UI3["display timer 2"].setStyleSheet("*{font-size: 24px; color: White;}")
        
        self.wdgts_UI3["timer 1"].timeout.connect(self.showtime_timer1)
        self.wdgts_UI3["timer 2"].timeout.connect(self.showtime_timer2)
        #self.wdgts_UI3["timer 1"].setInterval(1) # set the interval to 1 ms
        #self.wdgts_UI3["timer 2"].setInterval(1) # set the interval to 1 ms
        self.wdgts_UI3["timer 1"].start(10)
        self.wdgts_UI3["timer 2"].start(10)
        
        self.wdgts_UI3["board"].adjustSize()
        self.wdgts_UI3["label p1"].adjustSize()
        self.wdgts_UI3["label p2"].adjustSize()
        self.wdgts_UI3["label score p1"].adjustSize()
        self.wdgts_UI3["label score p2"].adjustSize()
        self.wdgts_UI3["score p1"].adjustSize()
        self.wdgts_UI3["score p2"].adjustSize()
        self.wdgts_UI3["label timer 1"].adjustSize()
        self.wdgts_UI3["label timer 2"].adjustSize()

        # Placing all the widgets in the main menu frame:
        grid = QGridLayout()
        grid.addWidget(self.wdgts_UI3["label p1"], 0, 0, 1, 2, alignment=QtCore.Qt.AlignCenter)
        grid.addWidget(self.wdgts_UI3["label score p1"], 1, 0, alignment=QtCore.Qt.AlignLeft)
        grid.addWidget(self.wdgts_UI3["score p1"], 1, 1, alignment=QtCore.Qt.AlignLeft)
        grid.addWidget(self.wdgts_UI3["label timer 1"], 2, 0, alignment=QtCore.Qt.AlignLeft)
        grid.addWidget(self.wdgts_UI3["display timer 1"], 2, 1, alignment=QtCore.Qt.AlignLeft)
        grid.addWidget(self.wdgts_UI3["label p2"], 0, 3, 1, 2, alignment=QtCore.Qt.AlignCenter)
        grid.addWidget(self.wdgts_UI3["label score p2"], 1, 3, alignment=QtCore.Qt.AlignLeft)
        grid.addWidget(self.wdgts_UI3["score p2"], 1, 4, alignment=QtCore.Qt.AlignLeft)
        grid.addWidget(self.wdgts_UI3["label timer 2"], 2, 3, alignment=QtCore.Qt.AlignLeft)
        grid.addWidget(self.wdgts_UI3["display timer 2"], 2, 4, alignment=QtCore.Qt.AlignLeft)
        grid.addWidget(self.wdgts_UI3["board"], 3, 1, 4, 4, alignment=QtCore.Qt.AlignLeft)
        grid.addWidget(self.wdgts_UI3["button quit"], 8, 1)
        grid.addWidget(self.wdgts_UI3["button backward"], 8, 2)
        grid.addWidget(self.wdgts_UI3["button forward"], 8, 3)
        self.stack3.setLayout(grid)


    def display(self,i):
        self.Stack.setCurrentIndex(i)


    def game_pvp(self):
        self.p1_type = "Human"
        self.p2_type = "Human"
        self.Stack.setCurrentIndex(1)


    def game_pva(self):
        self.p1_type = "Human"
        self.p2_type = "IA"
        self.Stack.setCurrentIndex(1)


    def game_back(self):
        self.p1_type = None
        self.p2_type = None
        self.player_1 = None
        self.player_2 = None
        for ii in range(1,7):
            CHARACTERS[f"character {ii}"]["check"] = False
            self.wdgts_UI2[f"character {ii}"].setStyleSheet(dct_stylesheet["character"])

        self.Stack.setCurrentIndex(0)


    def game_quit(self):
        self.p1_type = None
        self.p2_type = None
        self.player_1 = None
        self.player_2 = None
        
        for ii in range(1,7):
            CHARACTERS[f"character {ii}"]["check"] = False
            self.wdgts_UI2[f"character {ii}"].setStyleSheet(dct_stylesheet["character"])
        
        for ii in range(len(self.W_whitestones)):
            self.W_whitestones[ii].deleteLater()
        for ii in range(len(self.W_blackstones)):
            self.W_blackstones[ii].deleteLater()
        del(self.W_whitestones)
        del(self.W_blackstones)
        self.W_whitestones = []
        self.W_blackstones = []

        self.Stack.setCurrentIndex(0)


    def game_play(self):
        if (self.player_1 != None) and (self.player_2 != None):
            self.Stack.setCurrentIndex(2)


    def game_backward(self):
        raise NotImplementedError()


    def game_forward(self):
        raise NotImplementedError()


    def game_score(self):
        raise NotImplementedError()


    def showtime_timer1(self):
        if self.start_black:
            self.count_black += 10
            # getting and displaying text from count
            self.wdgts_UI3["display timer 1"].setText(str(self.count_black / 1000) + " s")

    def showtime_timer2(self):
        if self.start_white:
            self.count_white += 10
            self.wdgts_UI3["display timer 2"].setText(str(self.count_white / 1000) + " s")


    def select_character_1(self):
        if CHARACTERS["character 1"]["check"] == False:
            if self.player_1 == None:
                self.player_1 = CHARACTERS["character 1"]
                self.wdgts_UI2["character 1"].setStyleSheet("*{background-color : blue;}")
                CHARACTERS["character 1"]["check"] = True
            elif self.player_2 == None:
                self.player_2 = CHARACTERS["character 1"]
                self.wdgts_UI2["character 1"].setStyleSheet("*{background-color : red;}")
                CHARACTERS["character 1"]["check"] = True
        else:
            if self.player_1 == CHARACTERS["character 1"]:
                self.player_1 = None
            elif self.player_2 == CHARACTERS["character 1"]:
                self.player_2 = None
            CHARACTERS["character 1"]["check"] = False
            self.wdgts_UI2["character 1"].setStyleSheet(dct_stylesheet["character"])


    def select_character_2(self):
        if CHARACTERS["character 2"]["check"] == False:
            if self.player_1 == None:
                self.player_1 = CHARACTERS["character 2"]
                self.wdgts_UI2["character 2"].setStyleSheet("*{background-color : blue;}")
                CHARACTERS["character 2"]["check"] = True
            elif self.player_2 == None:
                self.player_2 = CHARACTERS["character 2"]
                self.wdgts_UI2["character 2"].setStyleSheet("*{background-color : red;}")
                CHARACTERS["character 2"]["check"] = True
        else:
            if self.player_1 == CHARACTERS["character 2"]:
                self.player_1 = None
            elif self.player_2 == CHARACTERS["character 2"]:
                self.player_2 = None
            CHARACTERS["character 2"]["check"] = False
            self.wdgts_UI2["character 2"].setStyleSheet(dct_stylesheet["character"])


    def select_character_3(self):
        if CHARACTERS["character 3"]["check"] == False:
            if self.player_1 == None:
                self.player_1 = CHARACTERS["character 3"]
                self.wdgts_UI2["character 3"].setStyleSheet("*{background-color : blue;}")
                CHARACTERS["character 3"]["check"] = True
            elif self.player_2 == None:
                self.player_2 = CHARACTERS["character 3"]
                self.wdgts_UI2["character 3"].setStyleSheet("*{background-color : red;}")
                CHARACTERS["character 3"]["check"] = True
        else:
            if self.player_1 == CHARACTERS["character 3"]:
                self.player_1 = None
            elif self.player_2 == CHARACTERS["character 3"]:
                self.player_2 = None
            CHARACTERS["character 3"]["check"] = False
            self.wdgts_UI2["character 3"].setStyleSheet(dct_stylesheet["character"])


    def select_character_4(self):
        if CHARACTERS["character 4"]["check"] == False:
            if self.player_1 == None:
                self.player_1 = CHARACTERS["character 4"]
                self.wdgts_UI2["character 4"].setStyleSheet("*{background-color : blue;}")
                CHARACTERS["character 4"]["check"] = True
            elif self.player_2 == None:
                self.player_2 = CHARACTERS["character 4"]
                self.wdgts_UI2["character 4"].setStyleSheet("*{background-color : red;}")
                CHARACTERS["character 4"]["check"] = True
        else:
            if self.player_1 == CHARACTERS["character 4"]:
                self.player_1 = None
            elif self.player_2 == CHARACTERS["character 4"]:
                self.player_2 = None
            CHARACTERS["character 4"]["check"] = False
            self.wdgts_UI2["character 4"].setStyleSheet(dct_stylesheet["character"])


    def select_character_5(self):
        if CHARACTERS["character 5"]["check"] == False:
            if self.player_1 == None:
                self.player_1 = CHARACTERS["character 5"]
                self.wdgts_UI2["character 5"].setStyleSheet("*{background-color : blue;}")
                CHARACTERS["character 5"]["check"] = True
            elif self.player_2 == None:
                self.player_2 = CHARACTERS["character 5"]
                self.wdgts_UI2["character 5"].setStyleSheet("*{background-color : red;}")
                CHARACTERS["character 5"]["check"] = True
        else:
            if self.player_1 == CHARACTERS["character 5"]:
                self.player_1 = None
            elif self.player_2 == CHARACTERS["character 5"]:
                self.player_2 = None
            CHARACTERS["character 5"]["check"] = False
            self.wdgts_UI2["character 5"].setStyleSheet(dct_stylesheet["character"])


    def select_character_6(self):
        if CHARACTERS["character 6"]["check"] == False:
            if self.player_1 == None:
                self.player_1 = CHARACTERS["character 6"]
                self.wdgts_UI2["character 6"].setStyleSheet("*{background-color : blue;}")
                CHARACTERS["character 6"]["check"] = True
            elif self.player_2 == None:
                self.player_2 = CHARACTERS["character 6"]
                self.wdgts_UI2["character 6"].setStyleSheet("*{background-color : red;}")
                CHARACTERS["character 6"]["check"] = True
        else:
            if self.player_1 == CHARACTERS["character 6"]:
                self.player_1 = None
            elif self.player_2 == CHARACTERS["character 6"]:
                self.player_2 = None
            CHARACTERS["character 6"]["check"] = False
            self.wdgts_UI2["character 6"].setStyleSheet(dct_stylesheet["character"])

    def mousePressEvent(self, event):
        raise NotImplementedError()


def window(mywindow:MyWindow):
    app = QApplication(sys.argv)
    if mywindow is None:
        win = MyWindow()
    else:
        win = mywindow

    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    #mywindow = MyWindow()
    window(None)