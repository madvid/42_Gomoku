from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLabel, QVBoxLayout, QWidget
import sys

class MyWindow(QMainWindow):
	def __init__(self):
		super(MyWindow, self).__init__()
		self.setWindowTitle("Gomoku by mdavid & ppeigne")
		self.setGeometry(200, 200, 1080, 720)
		print("height", self.geometry().height())
		print("width", self.geometry().width())
		self.initUI()

	def game_pvp():
		pass

	def game_pva1():
		pass

	def game_pva2():
		pass

	def initUI(self):
		# buttons and label
		self.button_pvp = QPushButton("Player vs Player", self)
		self.button_pva1 = QPushButton("Player vs Algo 1", self)
		self.button_pva2 = QPushButton("Player vs Algo 2", self)

		self.button_pvp.setGeometry(360, 160, 360, 80)
		self.button_pva1.setGeometry(360, 320, 360, 80)
		self.button_pva2.setGeometry(360, 480, 360, 80)

		self.button_pvp.clicked.connect(self.game_pvp)
		self.button_pva1.clicked.connect(self.game_pva1)
		self.button_pva2.clicked.connect(self.game_pva2)

		#self.button_pvp.setStyleSheet("assets/button_pvp.png")
		#self.button_pva.setStyleSheet("assets/button_pva.png")
		
	def update(self):
		# self.label.adjustSize()
		pass

	# the events: press button, click with cursor ...

def window():
	app = QtWidgets.QApplication(sys.argv)
	win = MyWindow()
	win.show()
	sys.exit(app.exec())

if __name__ == "__main__":
	window()