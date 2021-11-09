import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLabel, QVBoxLayout, QWidget, QGridLayout
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QCursor


dct_stylesheet = {"menu_button": "*{border: 4px solid '#1B5DBF';" + 
								 "border-radius: 45px;" +
								 "font-size: 35px;" +
								 "color: white;" +
								 "padding: 25px 0;" +
								 "margin: 10px 20px;}" +
								 "*:hover{background: '#0067FF';}",
				  "character": "*{border: 4px solid '#1B5DBF';" + 
								 "border-radius: 0px;" +
								 "font-size: 20px;" +
								 "color: white;" +
								 "padding: 15px 0;" +
								 "margin: 5px 5px;}" +
								 "*:hover{background: '#0067FF';}",
				  "choose_frame": "*{border: 4px solid '#1B5DBF';" + 
								  "border-radius: 0px;" +
								  "font-size: 20px;" +
								  "color: white;" +
								  "padding: 15px 0;" +
								  "margin: 5px 5px;}" +
								  "*:hover{background: '#0067FF';}"}


class MyWindow(QWidget):
	def __init__(self):
		super(MyWindow, self).__init__()
		self.setWindowTitle("Gomoku by mdavid & ppeigne")
		self.setGeometry(200, 200, 1080, 720)
		self.setStyleSheet("background: #152338;")
		self.grid = QGridLayout()
		self.initUI()
		self.menu_frame()
		#self.select_frame()
		self.setLayout(self.grid)


	def initUI(self):
		# -------- MAIN MENU FRAME -------- #
		# Display logo
		image_main = QPixmap("assets/Gomoku.png")
		self.logo_main = QLabel()
		self.logo_main.setPixmap(image_main)
		self.logo_main.setAlignment(QtCore.Qt.AlignCenter)
		self.logo_main.setStyleSheet("margin-top: 0px;")
		
		# Button and Label widgets
		self.button_pvp = QPushButton("Player vs Player")
		self.button_pva = QPushButton("Player vs Algo 1")

		self.button_pvp.setGeometry(360, 160, 360, 80)
		self.button_pva.setGeometry(360, 320, 360, 80)

		self.button_pvp.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
		self.button_pva.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
		self.button_pvp.setStyleSheet(dct_stylesheet["menu_button"])
		self.button_pva.setStyleSheet(dct_stylesheet["menu_button"])

		#self.button_pvp.clicked.connect(self.game_pvp)
		#self.button_pva.clicked.connect(self.game_pva)

		# -------- SELECT PERSO FRAME -------- #
		# Display logo
		image_select = QPixmap("assets/character_selection.png")
		self.logo_select = QLabel()
		self.logo_select.setPixmap(image_select)
		self.logo_select.setAlignment(QtCore.Qt.AlignCenter)
		self.logo_select.setStyleSheet("margin-top: 0px;")
		
		# Buttons widget:
		self.button_player1 = QPushButton("Perso 1")
		self.button_player2 = QPushButton("Perso 2")
		self.button_player3 = QPushButton("Perso 3")
		self.button_player4 = QPushButton("Perso 4")
		self.button_player5 = QPushButton("Perso 5")
		self.button_player6 = QPushButton("Perso 6")
		self.button_play = QPushButton("PLAY")
		self.button_back = QPushButton("BACK")
		
		self.button_player1.setFixedWidth(200)
		self.button_player1.setFixedHeight(200)
		self.button_player2.setFixedWidth(200)
		self.button_player2.setFixedHeight(200)
		self.button_player3.setFixedWidth(200)
		self.button_player3.setFixedHeight(200)
		self.button_player4.setFixedWidth(200)
		self.button_player4.setFixedHeight(200)
		self.button_player5.setFixedWidth(200)
		self.button_player5.setFixedHeight(200)
		self.button_player6.setFixedWidth(200)
		self.button_player6.setFixedHeight(200)

		self.button_player1.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
		self.button_player2.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
		self.button_player3.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
		self.button_player4.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
		self.button_player5.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
		self.button_player6.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
		self.button_play.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
		self.button_back.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

		self.button_player1.setStyleSheet(dct_stylesheet["character"])
		self.button_player2.setStyleSheet(dct_stylesheet["character"])
		self.button_player3.setStyleSheet(dct_stylesheet["character"])
		self.button_player4.setStyleSheet(dct_stylesheet["character"])
		self.button_player5.setStyleSheet(dct_stylesheet["character"])
		self.button_player6.setStyleSheet(dct_stylesheet["character"])
		self.button_play.setStyleSheet(dct_stylesheet["choose_frame"])
		self.button_back.setStyleSheet(dct_stylesheet["choose_frame"])
	
	def menu_frame(self):
		#self.initUI()
		# Placing all the widgets in the main menu frame:
		self.grid.addWidget(self.logo_main, 0, 0)
		self.grid.addWidget(self.button_pvp, 1, 0)
		self.grid.addWidget(self.button_pva, 2, 0)
	
	def select_frame(self):
		# Placing all the widgets in the select character frame:
		self.grid.addWidget(self.logo_select, 0, 0, 1, 3)
		self.grid.addWidget(self.button_player1, 2, 0)
		self.grid.addWidget(self.button_player2, 2, 1)
		self.grid.addWidget(self.button_player3, 2, 2)
		self.grid.addWidget(self.button_player4, 3, 0)
		self.grid.addWidget(self.button_player5, 3, 1)
		self.grid.addWidget(self.button_player6, 3, 2)
		
		self.grid.addWidget(self.button_play, 4, 0)
		self.grid.addWidget(self.button_back, 4, 2)
	
	def game_pvp():
		pass

	def game_pva():
		pass
		

def window():
	app = QApplication(sys.argv)
	win = MyWindow()

	win.show()
	sys.exit(app.exec())

if __name__ == "__main__":
	window()