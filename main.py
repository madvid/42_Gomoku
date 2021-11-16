import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLabel, QVBoxLayout, QWidget, QGridLayout, QStackedWidget, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QCursor
import numpy as np
import numpy.typing as npt
from math import fabs
from typing import Tuple


W_WIDTH = 1080
W_HEIGHT = 720
MAIN_BTN_WIDTH = int(0.15 * W_WIDTH)
MAIN_BTN_HEIGHT = int(0.8 * W_HEIGHT)
WIDGETS_WH = {"stack1_logo": [int(W_WIDTH), int(0.4 * W_HEIGHT)],
              "stack1_pvp": [int(0.8 * W_WIDTH), int(0.15 * W_HEIGHT)],
              "stack1_pva": [int(0.8 * W_WIDTH), int(0.15 * W_HEIGHT)],
              "stack2_logo": [int(W_WIDTH), int(W_HEIGHT / 6.)],
              "stack2_character": [int(0.32 * W_HEIGHT), int(0.32 * W_HEIGHT)],
                "stack2_imgcharacter": [int(0.28 * W_HEIGHT), int(0.28 * W_HEIGHT)],
              "stack2_back": [int(W_WIDTH / 6.), int(W_HEIGHT / 6.)],
              "stack2_play": [int(W_WIDTH / 6.), int(W_HEIGHT / 6.)],
              "stack3_board": [int(4. * W_WIDTH / 6.), int(4. * W_HEIGHT / 6.)],
              "stack3_player": [int(2. * W_WIDTH / 6.), int(W_HEIGHT / 6.)],
              "stack3_lscore": [int(W_WIDTH / 6.), int(W_HEIGHT / 6.)],
              "stack3_score": [int(W_WIDTH / 6.), int(W_HEIGHT / 6.)],
              "stack3_quit": [int(2. * W_WIDTH / 6.), int(W_HEIGHT / 6.)]}

CHARACTERS = {"character_1":{"name":"Elon Musk", "file":"assets/pixel_elon.png", "check": False},
              "character_2":{"name":"Lee Sedol", "file":"assets/pixel_lee_sedol.png", "check": False},
              "character_3":{"name":"Sophie Viger", "file":"assets/pixel_sophie.png", "check": False},
              "character_4":{"name":"Matthieu David", "file":"assets/pixel_mdavid.png", "check": False},
              "character_5":{"name":"Pierre Peigne", "file":"assets/pixel_ppeigne.png", "check": False},
              "character_6":{"name":"Richard Feynman", "file":"assets/pixel_feynman.png", "check": False},}

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
                                "*:hover{background: 'red';}"}

nodes_x , nodes_y = 31 * np.arange(1, 20), 31 * np.arange(1, 20)
coords = np.array(np.meshgrid(nodes_x, nodes_y)).T.reshape(-1,2)


board = np.zeros((19, 19))

def nearest_coord(point:npt.NDArray[np.int_]) -> npt.NDArray[np.int_]:
    ii = point[0] // 31
    jj = point[1] // 31
    if fabs(point[0] - ii * 31) >  fabs(point[0] - (ii + 1) * 31):
        ii += 1
    if fabs(point[1] - jj * 31) >  fabs(point[1] - (jj + 1) * 31):
        jj += 1
    return np.array([ii * 31, jj * 31]) 


def stone_to_board(coord:Tuple[int, int], color:int):
    board[(coord[1] // 31) - 1, (coord[0] // 31) - 1] = color


class MyWindow(QWidget):

    def __init__(self):
        super(MyWindow, self).__init__()

        self.setWindowTitle("Gomoku by mdavid & ppeigne")
        #self.setGeometry(200, 200, 1080, 720)
        self.setFixedWidth(W_WIDTH)
        self.setFixedHeight(W_HEIGHT)
        self.setStyleSheet("background: #152338;")

        self.stone = 1 # 1 is white and -1 is black
        self.whitestone = []
        self.blackstone = []

        self.player_1 = None
        self.player_2 = None
        self.stack1 = QWidget()
        self.stack2 = QWidget()
        self.stack3 = QWidget()

        self.stack1UI()
        self.stack2UI()
        self.stack3UI()

        self.Stack = QStackedWidget (self)
        self.Stack.addWidget (self.stack1)
        self.Stack.addWidget (self.stack2)
        self.Stack.addWidget (self.stack3)


    def stack1UI(self):
        # -------- MAIN MENU FRAME -------- #
        # Label (logo) widget
        image_main = QPixmap("assets/Gomoku.png")
        self.logo_main = QLabel()
        self.logo_main.setPixmap(image_main)
        self.logo_main.setAlignment(QtCore.Qt.AlignCenter)
        self.logo_main.setStyleSheet("margin-top: 0px;")
        self.logo_main.resize(*WIDGETS_WH["stack1_logo"])

        # Button widgets
        self.button_pvp = QPushButton("")
        self.button_pva = QPushButton("")
        self.button_pvp.setStyleSheet(dct_stylesheet["menu_button"])
        self.button_pva.setStyleSheet(dct_stylesheet["menu_button"])

        self.button_pvp.setIcon(QtGui.QIcon('assets/Player_vs_Player.png'))
        self.button_pva.setIcon(QtGui.QIcon('assets/Player_vs_IA.png'))

        self.button_pvp.setIconSize(QtCore.QSize(640,50))
        self.button_pva.setIconSize(QtCore.QSize(640,50))
        self.button_pvp.resize(*WIDGETS_WH["stack1_pvp"])
        self.button_pva.resize(*WIDGETS_WH["stack1_pva"])

        self.button_pvp.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.button_pva.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

        # Connecting button signals to corresponding slots
        self.button_pvp.clicked.connect(self.game_pvp)
        self.button_pva.clicked.connect(self.game_pva)

        # Placing menu widgets in vertical layout:
        vlayout = QVBoxLayout()
        #vlayout.setAlignment(QtCore.Qt.AlignCenter)
        vlayout.addStretch(1)
        vlayout.addWidget(self.logo_main)
        vlayout.addStretch(2)
        vlayout.addWidget(self.button_pvp)
        vlayout.addStretch(0)
        vlayout.addWidget(self.button_pva)
        vlayout.addStretch(0)

        # Placing the vertical layout into a horizontal layout (centering ?)
        layout = QHBoxLayout()
        layout.addStretch(1)
        layout.addLayout(vlayout)
        layout.addStretch(1)
        self.stack1.setLayout(layout)



    def stack2UI(self):
        # -------- SELECT PERSO FRAME -------- #
        # Display logo
        image_select = QPixmap("assets/character_selection.png")
        self.logo_select = QLabel()
        self.logo_select.setPixmap(image_select)
        self.logo_select.setAlignment(QtCore.Qt.AlignCenter)
        self.logo_select.setStyleSheet("margin-top: 0px;")
        self.logo_select.setFixedSize(QtCore.QSize(*WIDGETS_WH["stack2_logo"]))

        # Buttons widget:
        self.character_1 = QPushButton("")
        self.character_2 = QPushButton("")
        self.character_3 = QPushButton("")
        self.character_4 = QPushButton("")
        self.character_5 = QPushButton("")
        self.character_6 = QPushButton("")
        self.character_1.setIcon(QtGui.QIcon(CHARACTERS["character_1"]["file"]))
        self.character_2.setIcon(QtGui.QIcon(CHARACTERS["character_2"]["file"]))
        self.character_3.setIcon(QtGui.QIcon(CHARACTERS["character_3"]["file"]))
        self.character_4.setIcon(QtGui.QIcon(CHARACTERS["character_4"]["file"]))
        self.character_5.setIcon(QtGui.QIcon(CHARACTERS["character_5"]["file"]))
        self.character_6.setIcon(QtGui.QIcon(CHARACTERS["character_6"]["file"]))
        self.character_1.setIconSize(QtCore.QSize(*WIDGETS_WH["stack2_imgcharacter"]))
        self.character_2.setIconSize(QtCore.QSize(*WIDGETS_WH["stack2_imgcharacter"]))
        self.character_3.setIconSize(QtCore.QSize(*WIDGETS_WH["stack2_imgcharacter"]))
        self.character_4.setIconSize(QtCore.QSize(*WIDGETS_WH["stack2_imgcharacter"]))
        self.character_5.setIconSize(QtCore.QSize(*WIDGETS_WH["stack2_imgcharacter"]))
        self.character_6.setIconSize(QtCore.QSize(*WIDGETS_WH["stack2_imgcharacter"]))


        self.button_play = QPushButton("")
        self.button_back = QPushButton("")
        self.button_play.setIcon(QtGui.QIcon('assets/PLAY.png'))
        self.button_back.setIcon(QtGui.QIcon('assets/BACK.png'))
        self.button_play.setIconSize(QtCore.QSize(203,67))
        self.button_back.setIconSize(QtCore.QSize(203,67))


        self.character_1.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.character_2.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.character_3.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.character_4.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.character_5.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.character_6.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.button_play.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.button_back.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

        self.character_1.setStyleSheet(dct_stylesheet["character"])
        self.character_2.setStyleSheet(dct_stylesheet["character"])
        self.character_3.setStyleSheet(dct_stylesheet["character"])
        self.character_4.setStyleSheet(dct_stylesheet["character"])
        self.character_5.setStyleSheet(dct_stylesheet["character"])
        self.character_6.setStyleSheet(dct_stylesheet["character"])
        self.button_play.setStyleSheet(dct_stylesheet["play_btn"])
        self.button_back.setStyleSheet(dct_stylesheet["back_btn"])

        self.character_1.setFixedSize(QtCore.QSize(*WIDGETS_WH["stack2_character"]))
        self.character_2.setFixedSize(QtCore.QSize(*WIDGETS_WH["stack2_character"]))
        self.character_3.setFixedSize(QtCore.QSize(*WIDGETS_WH["stack2_character"]))
        self.character_4.setFixedSize(QtCore.QSize(*WIDGETS_WH["stack2_character"]))
        self.character_5.setFixedSize(QtCore.QSize(*WIDGETS_WH["stack2_character"]))
        self.character_6.setFixedSize(QtCore.QSize(*WIDGETS_WH["stack2_character"]))
        self.button_play.setFixedSize(210, 70)
        self.button_back.setFixedSize(210, 70)

        # Placing all the widgets in the select character frame:
        grid = QGridLayout()
        grid.addWidget(self.logo_select, 0, 0, 1, 6, alignment=QtCore.Qt.AlignCenter)
        grid.addWidget(self.character_1, 1, 0, 2, 2, alignment=QtCore.Qt.AlignRight)
        grid.addWidget(self.character_2, 1, 2, 2, 2, alignment=QtCore.Qt.AlignCenter)
        grid.addWidget(self.character_3, 1, 4, 2, 2, alignment=QtCore.Qt.AlignLeft)
        grid.addWidget(self.character_4, 3, 0, 2, 2, alignment=QtCore.Qt.AlignRight)
        grid.addWidget(self.character_5, 3, 2, 2, 2, alignment=QtCore.Qt.AlignCenter)
        grid.addWidget(self.character_6, 3, 4, 2, 2, alignment=QtCore.Qt.AlignLeft)
        grid.addWidget(self.button_play, 5, 4, 1, 2, alignment=QtCore.Qt.AlignCenter)
        grid.addWidget(self.button_back, 5, 0, 1, 2, alignment=QtCore.Qt.AlignCenter)


        self.character_1.clicked.connect(self.select_character_1)
        self.character_2.clicked.connect(self.select_character_2)
        self.character_3.clicked.connect(self.select_character_3)
        self.character_4.clicked.connect(self.select_character_4)
        self.character_5.clicked.connect(self.select_character_5)
        self.character_6.clicked.connect(self.select_character_6)
        self.button_play.clicked.connect(self.game_play)
        self.button_back.clicked.connect(self.game_back)

        self.stack2.setLayout(grid)

    def stack3UI(self):
        # -------- GAME FRAME -------- #
        # Display logo
        self.board = QLabel("")
        board = QPixmap("assets/board.png")
        board = board.scaled(606, 606)
        #board = board.scaled(606, 606, QtCore.Qt.KeepAspectRatio)
        self.board.setPixmap(board)

        self.label_p1 = QLabel("")
        self.label_p1.setPixmap(QPixmap("assets/Player1.png"))
        self.label_p2 = QLabel("")
        self.label_p2.setPixmap(QPixmap("assets/Player2.png"))

        self.label_score_p1 = QLabel("")
        self.label_score_p1.setPixmap(QPixmap("assets/Score.png"))
        self.label_score_p2 = QLabel("")
        self.label_score_p2.setPixmap(QPixmap("assets/Score.png"))

        self.score_p1 = QLabel("")
        self.score_p1.setPixmap(QPixmap("assets/0.png"))
        self.score_p2 = QLabel("")
        self.score_p2.setPixmap(QPixmap("assets/0.png"))

        self.button_quit = QPushButton("")
        self.button_quit.setIcon(QtGui.QIcon('assets/QUIT.png'))
        self.button_quit.setIconSize(QtCore.QSize(203,67))
        self.button_quit.setStyleSheet(dct_stylesheet["back_btn"])
        self.button_quit.clicked.connect(self.game_quit)

        self.board.adjustSize()
        self.label_p1.adjustSize()
        self.label_p2.adjustSize()
        self.label_score_p1.adjustSize()
        self.label_score_p2.adjustSize()
        self.score_p1.adjustSize()
        self.score_p2.adjustSize()

        # Placing all the widgets in the main menu frame:
        grid = QGridLayout()
        grid.addWidget(self.board, 0, 0, 4, 4)
        grid.addWidget(self.label_p1, 0, 5, 1, 2, alignment=QtCore.Qt.AlignLeft)
        grid.addWidget(self.label_score_p1, 1, 5, alignment=QtCore.Qt.AlignLeft)
        grid.addWidget(self.score_p1, 1, 6)
        grid.addWidget(self.label_p2, 2, 5, 1, 2, alignment=QtCore.Qt.AlignLeft)
        grid.addWidget(self.label_score_p2, 3, 5, alignment=QtCore.Qt.AlignLeft)
        grid.addWidget(self.score_p2, 3, 6)
        grid.addWidget(self.button_quit, 4, 2, 1, 2)
        self.stack3.setLayout(grid)


    def display(self,i):
        self.Stack.setCurrentIndex(i)


    def game_pvp(self):
        self.Stack.setCurrentIndex(1)


    def game_pva(self):
        self.Stack.setCurrentIndex(1)


    def game_back(self):
        self.Stack.setCurrentIndex(0)

    def game_quit(self):
        self.Stack.setCurrentIndex(0)


    def game_play(self):
        if (self.player_1 != None) and (self.player_2 != None):
            self.Stack.setCurrentIndex(2)


    def select_character_1(self):
        if CHARACTERS["character_1"]["check"] == False:
            if self.player_1 == None:
                self.player_1 = CHARACTERS["character_1"]
                self.character_1.setStyleSheet("*{background-color : blue;}")
                CHARACTERS["character_1"]["check"] = True
            elif self.player_2 == None:
                self.player_2 = CHARACTERS["character_1"]
                self.character_1.setStyleSheet("*{background-color : red;}")
                CHARACTERS["character_1"]["check"] = True
        else:
            if self.player_1 == CHARACTERS["character_1"]:
                self.player_1 = None
            elif self.player_2 == CHARACTERS["character_1"]:
                self.player_2 = None
            CHARACTERS["character_1"]["check"] = False
            self.character_1.setStyleSheet(dct_stylesheet["character"])


    def select_character_2(self):
        if CHARACTERS["character_2"]["check"] == False:
            if self.player_1 == None:
                self.player_1 = CHARACTERS["character_2"]
                self.character_2.setStyleSheet("*{background-color : blue;}")
                CHARACTERS["character_2"]["check"] = True
            elif self.player_2 == None:
                self.player_2 = CHARACTERS["character_2"]
                self.character_2.setStyleSheet("*{background-color : red;}")
                CHARACTERS["character_2"]["check"] = True
        else:
            if self.player_1 == CHARACTERS["character_2"]:
                self.player_1 = None
            elif self.player_2 == CHARACTERS["character_2"]:
                self.player_2 = None
            CHARACTERS["character_2"]["check"] = False
            self.character_2.setStyleSheet(dct_stylesheet["character"])


    def select_character_3(self):
        if CHARACTERS["character_3"]["check"] == False:
            if self.player_1 == None:
                self.player_1 = CHARACTERS["character_3"]
                self.character_3.setStyleSheet("*{background-color : blue;}")
                CHARACTERS["character_3"]["check"] = True
            elif self.player_2 == None:
                self.player_2 = CHARACTERS["character_3"]
                self.character_3.setStyleSheet("*{background-color : red;}")
                CHARACTERS["character_3"]["check"] = True
        else:
            if self.player_1 == CHARACTERS["character_3"]:
                self.player_1 = None
            elif self.player_2 == CHARACTERS["character_3"]:
                self.player_2 = None
            CHARACTERS["character_3"]["check"] = False
            self.character_3.setStyleSheet(dct_stylesheet["character"])


    def select_character_4(self):
        if CHARACTERS["character_4"]["check"] == False:
            if self.player_1 == None:
                self.player_1 = CHARACTERS["character_4"]
                self.character_4.setStyleSheet("*{background-color : blue;}")
                CHARACTERS["character_4"]["check"] = True
            elif self.player_2 == None:
                self.player_2 = CHARACTERS["character_4"]
                self.character_4.setStyleSheet("*{background-color : red;}")
                CHARACTERS["character_4"]["check"] = True
        else:
            if self.player_1 == CHARACTERS["character_4"]:
                self.player_1 = None
            elif self.player_2 == CHARACTERS["character_4"]:
                self.player_2 = None
            CHARACTERS["character_4"]["check"] = False
            self.character_4.setStyleSheet(dct_stylesheet["character"])


    def select_character_5(self):
        if CHARACTERS["character_5"]["check"] == False:
            if self.player_1 == None:
                self.player_1 = CHARACTERS["character_5"]
                self.character_5.setStyleSheet("*{background-color : blue;}")
                CHARACTERS["character_5"]["check"] = True
            elif self.player_2 == None:
                self.player_2 = CHARACTERS["character_5"]
                self.character_5.setStyleSheet("*{background-color : red;}")
                CHARACTERS["character_5"]["check"] = True
        else:
            if self.player_1 == CHARACTERS["character_5"]:
                self.player_1 = None
            elif self.player_2 == CHARACTERS["character_5"]:
                self.player_2 = None
            CHARACTERS["character_5"]["check"] = False
            self.character_5.setStyleSheet(dct_stylesheet["character"])


    def select_character_6(self):
        if CHARACTERS["character_6"]["check"] == False:
            if self.player_1 == None:
                self.player_1 = CHARACTERS["character_6"]
                self.character_6.setStyleSheet("*{background-color : blue;}")
                CHARACTERS["character_6"]["check"] = True
            elif self.player_2 == None:
                self.player_2 = CHARACTERS["character_6"]
                self.character_6.setStyleSheet("*{background-color : red;}")
                CHARACTERS["character_6"]["check"] = True
        else:
            if self.player_1 == CHARACTERS["character_6"]:
                self.player_1 = None
            elif self.player_2 == CHARACTERS["character_6"]:
                self.player_2 = None
            CHARACTERS["character_6"]["check"] = False
            self.character_6.setStyleSheet(dct_stylesheet["character"])

    def mousePressEvent(self, event):
        def on_board(qpoint):
            x, y = qpoint.x(), qpoint.y()
            if (x >= 25) and (x <= 603) and (y >= 25) and (y <= 603):
                return True
            return False


        if (self.Stack.currentIndex() == 2) and on_board(event.pos()) and (event.buttons() == QtCore.Qt.LeftButton):
            current_stone =  QLabel("", self.board)
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
            
            stone_to_board(nearest, self.stone)
            self.stone = - self.stone
            #print(board)
            current_stone.move(int(1.02 * nearest[0]) - 26, int(1.02 * nearest[1]) - 26)
            #self.stack3.addWidget(current_stone)
            current_stone.show()


def window():
    app = QApplication(sys.argv)
    win = MyWindow()

    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    window()