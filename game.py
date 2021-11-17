# =========================================================================== #
# ____________________  |Importation des lib/packages|   ____________________ #
# =========================================================================== #
from interface.game_interface import mywindow
from game.minimax import solver
import numpy as np


class Game():
    def __init__(self):
        self.grid = np.zeros((19,19))
        self.mywindow = mywindow()
        self.agent = solver()