import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLabel, QVBoxLayout, QWidget, QGridLayout, QStackedWidget
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QCursor


W_WIDTH = 1080
W_HEIGHT = 720
MAIN_BTN_WIDTH = int(0.15 * W_WIDTH)
MAIN_BTN_HEIGHT = int(0.8 * W_HEIGHT)
MAIN_BTN_XY = {"pvp": [int(0.4 * W_WIDTH), int(0.5 * W_HEIGHT)],
			   "pva": [int(0.3 * W_WIDTH), int(0.95 * W_HEIGHT)]}

CHARACTERS = {"character_1":{"name":"Elon Musk", "file":"assets/pixel_elon.png", "check": False},
			  "character_2":{"name":"Lee Sedol", "file":"assets/pixel_lee_sedol.png", "check": False},
			  "character_3":{"name":"Sophie Viger", "file":"assets/pixel_sophie.png", "check": False},
			  "character_4":{"name":"Matthieu David", "file":"assets/pixel_mdavid.png", "check": False},
			  "character_5":{"name":"Pierre Peigne", "file":"assets/pixel_ppeigne.png", "check": False},
			  "character_6":{"name":"Richard Feynman", "file":"assets/pixel_feynman.png", "check": False},}

dct_stylesheet = {"menu_button": "*{border: 4px solid '#1B5DBF';" + 
								 "border-radius: 45px;" +
								 "font-size: 35px;" +
								 "color: white;" +
								 "padding: 25px 0;" +
								 "margin: 10px 20px;}" +
								 "*:hover{background: '#0067FF';}",
				"character": "*{border: 4px solid '#FFFFFF';" + 
								 "border-radius: 0px;" +
								 "font-size: 20px;" +
								 "color: white;" +
								 "padding: 0px 0px;" +
								 "margin: 0px 0px;}" +
								 "*:hover{background: '#00CC00';}",
				"choose_frame": "*{border: 4px solid '#1B5DBF';" + 
								"border-radius: 20px;" +
								"font-size: 20px;" +
								"color: white;" +
								"padding: 0px 0px;" +
								"margin: 0px 0px;}" +
								"*:hover{background: '#0067FF';}"}


class MyWindow(QWidget):

	def __init__(self):
		super(MyWindow, self).__init__()
		
		self.setWindowTitle("Gomoku by mdavid & ppeigne")
		#self.setGeometry(200, 200, 1080, 720)
		self.setFixedWidth(1080)
		self.setFixedHeight(720)
		self.setStyleSheet("background: #152338;")
		
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
		# Display logo
		image_main = QPixmap("assets/Gomoku.png")
		self.logo_main = QLabel()
		self.logo_main.setPixmap(image_main)
		self.logo_main.setAlignment(QtCore.Qt.AlignCenter)
		self.logo_main.setStyleSheet("margin-top: 0px;")
		
		# Button and Label widgets
		self.button_pvp = QPushButton("")
		self.button_pva = QPushButton("")
		self.button_pvp.setIcon(QtGui.QIcon('assets/Player_vs_Player.png'))
		self.button_pva.setIcon(QtGui.QIcon('assets/Player_vs_IA.png'))
		self.button_pvp.setIconSize(QtCore.QSize(640,50))
		self.button_pva.setIconSize(QtCore.QSize(640,50))

		self.button_pvp.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
		self.button_pva.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
		self.button_pvp.setStyleSheet(dct_stylesheet["menu_button"])
		self.button_pva.setStyleSheet(dct_stylesheet["menu_button"])
		self.button_pvp.setGeometry(MAIN_BTN_WIDTH, MAIN_BTN_HEIGHT, *MAIN_BTN_XY["pvp"])
		self.button_pva.setGeometry(MAIN_BTN_WIDTH, MAIN_BTN_HEIGHT, *MAIN_BTN_XY["pva"])

		self.button_pvp.clicked.connect(self.game_pvp)
		self.button_pva.clicked.connect(self.game_pva)
		grid = QGridLayout()

		# Placing all the widgets in the main menu frame:
		grid.addWidget(self.logo_main, 0, 0)
		grid.addWidget(self.button_pvp, 1, 0)
		grid.addWidget(self.button_pva, 2, 0)
		
		self.stack1.setLayout(grid)


	def stack2UI(self):
		# -------- SELECT PERSO FRAME -------- #
		# Display logo
		image_select = QPixmap("assets/character_selection.png")
		self.logo_select = QLabel()
		self.logo_select.setPixmap(image_select)
		self.logo_select.setAlignment(QtCore.Qt.AlignCenter)
		self.logo_select.setStyleSheet("margin-top: 0px;")
		
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
		self.character_1.setIconSize(QtCore.QSize(186,186))
		self.character_2.setIconSize(QtCore.QSize(186,186))
		self.character_3.setIconSize(QtCore.QSize(186,186))
		self.character_4.setIconSize(QtCore.QSize(186,186))
		self.character_5.setIconSize(QtCore.QSize(186,186))
		self.character_6.setIconSize(QtCore.QSize(186,186))
		
		self.button_play = QPushButton("")
		self.button_back = QPushButton("")
		self.button_play.setIcon(QtGui.QIcon('assets/PLAY.png'))
		self.button_back.setIcon(QtGui.QIcon('assets/BACK.png'))
		self.button_play.setIconSize(QtCore.QSize(192,67))
		self.button_back.setIconSize(QtCore.QSize(203,67))
		
		self.character_1.setFixedWidth(210)
		self.character_1.setFixedHeight(210)
		self.character_2.setFixedWidth(210)
		self.character_2.setFixedHeight(210)
		self.character_3.setFixedWidth(210)
		self.character_3.setFixedHeight(210)
		self.character_4.setFixedWidth(210)
		self.character_4.setFixedHeight(210)
		self.character_5.setFixedWidth(210)
		self.character_5.setFixedHeight(210)
		self.character_6.setFixedWidth(210)
		self.character_6.setFixedHeight(210)
		
		self.button_play.setFixedWidth(210)
		self.button_play.setFixedHeight(70)
		self.button_back.setFixedWidth(210)
		self.button_back.setFixedHeight(70)

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
		self.button_play.setStyleSheet(dct_stylesheet["choose_frame"])
		self.button_back.setStyleSheet(dct_stylesheet["choose_frame"])

		# Placing all the widgets in the select character frame:
		grid = QGridLayout()
		grid.addWidget(self.logo_select, 0, 0, 1, 3)
		grid.addWidget(self.character_1, 1, 0)
		grid.addWidget(self.character_2, 1, 1)
		grid.addWidget(self.character_3, 1, 2)
		grid.addWidget(self.character_4, 2, 0)
		grid.addWidget(self.character_5, 2, 1)
		grid.addWidget(self.character_6, 2, 2)
		
		grid.addWidget(self.button_play, 3, 2)
		grid.addWidget(self.button_back, 3, 0)

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
		# -------- MAIN MENU FRAME -------- #
		# Display logo
		self.label_p1 = QLabel("")
		self.label_p1.setPixmap(QPixmap("assets/Player1.png"))

		self.label_p2 = QLabel("")
		self.label_p2.setPixmap(QPixmap("assets/Player2.png"))

		self.label_score_p1 = QLabel("")
		self.label_score_p1.setPixmap(QPixmap("assets/Score.png"))

		self.label_score_p2 = QLabel("")
		self.label_score_p2.setPixmap(QPixmap("assets/Score.png"))

		self.board = QLabel("")
		self.board.setPixmap(QPixmap("assets/board.png"))

		self.score_p1 = QLabel("0")
		self.score_p2 = QLabel("0")


		grid = QGridLayout()
	
		# Placing all the widgets in the main menu frame:
		grid.addWidget(self.board, 0, 0, 4, 4)
		grid.addWidget(self.label_p1, 0, 4)
		grid.addWidget(self.label_score_p1, 1, 4)
		
		grid.addWidget(self.label_p2, 2, 4)
		grid.addWidget(self.label_score_p2, 3, 4)		
		self.stack3.setLayout(grid)

		
	def display(self,i):
		self.Stack.setCurrentIndex(i)


	def game_pvp(self):
		self.Stack.setCurrentIndex(1)


	def game_pva(self):
		self.Stack.setCurrentIndex(1)


	def game_back(self):
		self.Stack.setCurrentIndex(0)


	def game_play(self):
		self.Stack.setCurrentIndex(2)


	def select_character_1(self):
		if CHARACTERS["character_1"]["check"] == False:
			if self.player_1 == None:
				self.player_1 = CHARACTERS["character_1"]
				self.character_1.setStyleSheet("background-color : #0080ff")
			else:
				self.player_2 = CHARACTERS["character_1"]
				self.character_1.setStyleSheet("background-color : red")
			CHARACTERS["character_1"]["check"] = True
		else:
			if self.player_1 == CHARACTERS["character_1"]:
				self.player_1 = None
				# remettre le background original du bouton
			else:
				self.player_2 = None
				# remettre le background original du bouton
			CHARACTERS["character_1"]["check"] = False
			self.character_1.setStyleSheet("background-color : None")


	def select_character_2(self):
		if CHARACTERS["character_2"]["check"] == False:
			if self.player_1 == None:
				self.player_2 = CHARACTERS["character_2"]
				self.character_1.setStyleSheet("background-color : #0080ff")
			else:
				self.player_2 = CHARACTERS["character_2"]
				self.character_2.setStyleSheet("background-color : red")
			CHARACTERS["character_2"]["check"] = True
		else:
			if self.player_1 == CHARACTERS["character_1"]:
				self.player_1 = None
				# remettre le background original du bouton
			else:
				self.player_2 = None
				# remettre le background original du bouton
			CHARACTERS["character_2"]["check"] = False
			self.character_2.setStyleSheet("background-color : None")


	def select_character_3(self):
		if CHARACTERS["character_3"]["check"] == False:
			if self.player_1 == None:
				self.player_1 = CHARACTERS["character_3"]
				self.character_3.setStyleSheet("background-color : #0080ff")
			else:
				self.player_2 = CHARACTERS["character_3"]
				self.character_3.setStyleSheet("background-color : red")
			CHARACTERS["character_3"]["check"] = True
		else:
			if self.player_1 == CHARACTERS["character_3"]:
				self.player_1 = None
				# remettre le background original du bouton
			else:
				self.player_2 = None
				# remettre le background original du bouton
			CHARACTERS["character_3"]["check"] = False
			self.character_3.setStyleSheet("background-color : None")


	def select_character_4(self):
		if CHARACTERS["character_4"]["check"] == False:
			if self.player_1 == None:
				self.player_1 = CHARACTERS["character_4"]
				self.character_4.setStyleSheet("background-color : #0080ff")
			else:
				self.player_2 = CHARACTERS["character_4"]
				self.character_4.setStyleSheet("background-color : red")
			CHARACTERS["character_4"]["check"] = True
		else:
			if self.player_1 == CHARACTERS["character_1"]:
				self.player_1 = None
				# remettre le background original du bouton
			else:
				self.player_2 = None
				# remettre le background original du bouton
			CHARACTERS["character_4"]["check"] = False
			self.character_4.setStyleSheet("background-color : None")
	

	def select_character_5(self):
		if CHARACTERS["character_5"]["check"] == False:
			if self.player_1 == None:
				self.player_1 = CHARACTERS["character_5"]
				self.character_5.setStyleSheet("background-color : #0080ff")
			else:
				self.player_2 = CHARACTERS["character_5"]
				self.character_5.setStyleSheet("background-color : red")
			CHARACTERS["character_5"]["check"] = True
		else:
			if self.player_1 == CHARACTERS["character_5"]:
				self.player_1 = None
				# remettre le background original du bouton
			else:
				self.player_2 = None
				# remettre le background original du bouton
			CHARACTERS["character_5"]["check"] = False
			self.character_5.setStyleSheet("background-color : None")
	

	def select_character_6(self):
		if CHARACTERS["character_6"]["check"] == False:
			if self.player_1 == None:
				self.player_1 = CHARACTERS["character_6"]
				self.character_6.setStyleSheet("background-color : #0080ff")
			else:
				self.player_2 = CHARACTERS["character_6"]
				self.character_6.setStyleSheet("background-color : red")
			CHARACTERS["character_6"]["check"] = True
		else:
			if self.player_1 == CHARACTERS["character_6"]:
				self.player_1 = None
				# remettre le background original du bouton
			else:
				self.player_2 = None
				# remettre le background original du bouton
			CHARACTERS["character_6"]["check"] = False
			self.character_6.setStyleSheet("background-color : None")


def window():
	app = QApplication(sys.argv)
	win = MyWindow()

	win.show()
	sys.exit(app.exec())

if __name__ == "__main__":
	window()