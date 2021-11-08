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


class MyWindow(QMainWindow):
	def __init__(self):
		super(MyWindow, self).__init__()
		self.setWindowTitle("Gomoku by mdavid & ppeigne")
		self.setGeometry(200, 200, 1080, 720)
		print("height", self.geometry().height())
		print("width", self.geometry().width())
		self.setStyleSheet("background: #152338;")
		self.initUI()

	def initUI(self):
		# buttons and label
		self.button_pvp = QPushButton("Player vs Player", self)
		self.button_pva1 = QPushButton("Player vs Algo 1", self)
		self.button_pva2 = QPushButton("Player vs Algo 2", self)

		self.button_pvp.setGeometry(360, 160, 360, 80)
		self.button_pva1.setGeometry(360, 320, 360, 80)
		self.button_pva2.setGeometry(360, 480, 360, 80)

		# Display logo
		image = QPixmap("assets/Gomoku.png")
		logo = QLabel()
		logo.setPixmap(image)
		logo.setAlignment(QtCore.Qt.AlignCenter)
		logo.setStyleSheet("margin-top: 0px;")
		
		# Button widget:
		button_pvp = QPushButton("PLAY")
		button_pvp.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
		button_pvp.setStyleSheet(dct_stylesheet["menu_button"])
		grid.addWidget(logo, 0, 0)
		grid.addWidget(button_pvp, 1, 0)

		self.button_pvp.clicked.connect(self.game_pvp)
		self.button_pva1.clicked.connect(self.game_pva1)
		self.button_pva2.clicked.connect(self.game_pva2)
	
	def menu_frame(self):
		self.initUI()
	
	
		def game_pvp():
			pass

		def game_pva1():
			pass

		def game_pva2():
			pass
		

def window():
	app = QApplication(sys.argv)
	#win = MyWindow()
	win = QWidget()
	win.setWindowTitle("Gomoku by ppeigne and mdavid")
	#win.setFixedWidth(1000)
	win.setGeometry(200, 200, 1080, 720)

	grid = QGridLayout()

	def menu_frame():

	def select_perso_frame():
		# Display logo
		image = QPixmap("assets/character_selection.png")
		logo = QLabel()
		logo.setPixmap(image)
		logo.setAlignment(QtCore.Qt.AlignCenter)
		logo.setStyleSheet("margin-top: 0px;")
		# Buttons widget:
		button_player1 = QPushButton("Perso 1")
		button_player2 = QPushButton("Perso 2")
		button_player3 = QPushButton("Perso 3")
		button_player4 = QPushButton("Perso 4")
		button_player5 = QPushButton("Perso 5")
		button_player6 = QPushButton("Perso 6")
		button_play = QPushButton("PLAY")
		button_back = QPushButton("BACK")
		
		button_player1.setFixedWidth(200)
		button_player1.setFixedHeight(200)
		button_player2.setFixedWidth(200)
		button_player2.setFixedHeight(200)
		button_player3.setFixedWidth(200)
		button_player3.setFixedHeight(200)
		button_player4.setFixedWidth(200)
		button_player4.setFixedHeight(200)
		button_player5.setFixedWidth(200)
		button_player5.setFixedHeight(200)
		button_player6.setFixedWidth(200)
		button_player6.setFixedHeight(200)

		button_player1.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
		button_player2.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
		button_player3.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
		button_player4.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
		button_player5.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
		button_player6.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
		button_play.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
		button_back.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

		button_player1.setStyleSheet(dct_stylesheet["character"])
		button_player2.setStyleSheet(dct_stylesheet["character"])
		button_player3.setStyleSheet(dct_stylesheet["character"])
		button_player4.setStyleSheet(dct_stylesheet["character"])
		button_player5.setStyleSheet(dct_stylesheet["character"])
		button_player6.setStyleSheet(dct_stylesheet["character"])
		button_play.setStyleSheet(dct_stylesheet["choose_frame"])
		button_back.setStyleSheet(dct_stylesheet["choose_frame"])
		
		grid.addWidget(logo, 0, 0, 1, 3)
		
		grid.addWidget(button_player1, 2, 0)
		grid.addWidget(button_player2, 2, 1)
		grid.addWidget(button_player3, 2, 2)
		grid.addWidget(button_player4, 3, 0)
		grid.addWidget(button_player5, 3, 1)
		grid.addWidget(button_player6, 3, 2)
		
		grid.addWidget(button_play, 4, 0)
		grid.addWidget(button_back, 4, 2)

	#menu_frame()
	select_perso_frame()

	win.setLayout(grid)
	win.show()
	sys.exit(app.exec())

if __name__ == "__main__":
	window()