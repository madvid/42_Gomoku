# =========================================================================== #
# ____________________  |Importation des lib/packages|   ____________________ #
# =========================================================================== #
import numpy as np

# =========================================================================== #
#                          | constants definition |                           #
# =========================================================================== #
# Encoding the color of the stones.
BLACK = 1
WHITE = -1

# kernels to check if there is capture
k_diag1 = np.array([[[-1, 0,  0,  0],
                     [0,  1,  0,  0],
                     [0,  0,  1,  0],
                     [0,  0,  0, -1]]])

k_diag2 = np.array([[[0,  0, 0, -1],
                     [0,  0, 1,  0],
                     [0,  1, 0,  0],
                     [-1, 0, 0,  0]]])


k_line = np.array([[[-1, 1, 1, -1]]])
k_col = np.array([[[1], [1], [1], [1]]])
k_captures = {"line": k_line, "column": k_col, "diag1": k_diag1, "diag2": k_diag2}

# kernels to check if there is a free three
k_freethree = np.array([1, 2, 2, 2, 2, 1])

# Pixel coordinates of the top left and bottom right corners of the board
TOP_LEFT_X = 229 
TOP_LEFT_Y = 210
BOTTOM_RIGHT_X = 836
BOTTOM_RIGHT_Y = 817