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
