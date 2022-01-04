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
k_diag = np.array([[BLACK, 0,     0,     0],
                   [0,     WHITE, 0,     0],
                   [0,     0,     WHITE, 0],
                   [0,     0,     0,     BLACK]])

k_line = np.array([[BLACK, WHITE, WHITE, BLACK]])

k_captures = {"line": k_line, "column": np.rot90(k_line), "diag1": k_diag, "diag2": np.rot90(k_diag)}

# kernels to check if there is a free three
k_freethree = np.array([1, 2, 2, 2, 2, 1])

# Pixel coordinates of the top left and bottom right corners of the board
TOP_LEFT_X = 229 
TOP_LEFT_Y = 210
BOTTOM_RIGHT_X = 836
BOTTOM_RIGHT_Y = 817