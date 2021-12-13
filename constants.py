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
k_diags = np.array([np.array([[BLACK, 0,     0,     0],
                              [0,     WHITE, 0,     0],
                              [0,     0,     WHITE, 0],
                              [0,     0,     0,     BLACK]]),
                    np.array([[0,     0,     0,     BLACK],
                              [0,     0,     WHITE, 0],
                              [0,     WHITE, 0,     0],
                              [BLACK, 0,     0,     0]])])

k_lines = [np.array([[BLACK, WHITE, WHITE, BLACK]]),
           np.array([[BLACK],
                     [WHITE],
                     [WHITE],
                     [BLACK]])]

k_capture_l = np.array([[BLACK],[WHITE],[0],[BLACK]])
k_capture_d = np.array([[BLACK, 0,     0, 0],
                        [0,     WHITE, 0, 0],
                        [0,     0,     0, 0],
                        [0,     0,     0, BLACK]])

k_captures = [k_capture_l, np.rot90(k_capture_l), np.rot90(k_capture_l, k=2), np.rot90(k_capture_l, k=3),
              -k_capture_l, np.rot90(-k_capture_l), -np.rot90(k_capture_l, k=2), -np.rot90(k_capture_l, k=3),
              k_capture_d, np.rot90(k_capture_d), np.rot90(k_capture_d, k=2), np.rot90(k_capture_d, k=3),
              -k_capture_d, np.rot90(-k_capture_d), -np.rot90(k_capture_d, k=2), -np.rot90(k_capture_d, k=3)]

# kernels to check if there is a free three
k_freethree_l = np.array([[1, 2, 2, 2, 2, 1]])
k_freethree_d = np.array([[1, 0, 0, 0, 0, 0],
                          [0, 2, 0, 0, 0, 0],
                          [0, 0, 2, 0, 0, 0],
                          [0, 0, 0, 2, 0, 0],
                          [0, 0, 0, 0, 2, 0],
                          [0, 0, 0, 0, 0, 1]])
k_free_threes = [k_freethree_l, np.rot90(k_freethree_l), k_freethree_d, np.rot90(k_freethree_d)]