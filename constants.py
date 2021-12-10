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

# kernels to check if there is a double free threes
S = 1 # choose a number corresponding to what the stone will be multiply by
V = 1 # choose a number corresponding to what the empty position will be multiply by
s1_a = np.array([[V, 0, 0, 0, 0, 0, 0],
				 [0, S, 0, 0, 0, 0, 0],
				 [0, 0, S, 0, 0, 0, 0],
				 [0, 0, V, S, S, S, V],
				 [0, 0, 0, 0, V, 0, 0]])
s1_b = np.array([[0, V, 0, 0, 0],
				 [0, S, 0, 0, 0],
				 [0, S, 0, 0, 0],
				 [V, S, S, S, V],
				 [0, V, 0, 0, 0]])
s1_c = np.array([[0, 0, 0, 0, V],
				 [0, 0, 0, S, 0],
				 [0, 0, S, 0, 0],
				 [V, S, S, S, V],
				 [V, 0, 0, 0, 0]])
s1_d = np.array([[V, 0, 0, 0, 0, 0, V],
				 [0, S, 0, 0, 0, S, 0],
				 [0, 0, S, 0, S, 0, 0],
				 [0, 0, 0, S, 0, 0, 0],
				 [0, 0, V, 0, V, 0, 0]])

s2_a = np.array([[V, 0, 0, 0, 0, 0, 0, 0],
				 [0, S, 0, 0, 0, 0, 0, 0],
				 [0, 0, S, 0, 0, 0, 0, 0],
				 [0, 0, 0, V, 0, 0, 0, 0],
				 [0, 0, 0, V, S, S, S, V],
				 [0, 0, 0, 0, 0, V, 0, 0]])
s2_b = np.array([[0, V, 0, 0, 0],
				 [0, S, 0, 0, 0],
				 [0, S, 0, 0, 0],
				 [0, V, 0, 0, 0],
				 [V, S, S, S, V],
				 [0, V, 0, 0, 0]])
s2_c = np.array([[0, 0, 0, 0, 0, V],
				 [0, 0, 0, 0, S, 0],
				 [0, 0, 0, S, 0, 0],
				 [0, 0, V, 0, 0, 0],
				 [V, S, S, S, V, 0],
				 [V, 0, 0, 0, 0, 0]])
s2_d = np.array([[V, 0, 0, 0, 0, 0, 0, 0],
				 [0, S, 0, 0, 0, 0, 0, V],
				 [0, 0, S, 0, 0, 0, S, 0],
				 [0, 0, 0, V, 0, S, 0, 0],
				 [0, 0, 0, 0, S, 0, 0, 0],
				 [0, 0, 0, V, 0, V, 0, 0]])

s3_a = np.array([[V, 0, 0, 0, 0, 0, 0, 0],
				 [0, S, 0, 0, 0, 0, 0, 0],
				 [0, 0, V, 0, 0, 0, 0, 0],
				 [0, 0, 0, S, 0, 0, 0, 0],
				 [0, 0, 0, V, S, S, S, V],
				 [0, 0, 0, 0, 0, V, 0, 0]])
s3_b = np.array([[0, V, 0, 0, 0],
				 [0, S, 0, 0, 0],
				 [0, V, 0, 0, 0],
				 [0, S, 0, 0, 0],
				 [V, S, S, S, V],
				 [0, V, 0, 0, 0]])
s3_c = np.array([[0, 0, 0, 0, 0, V],
				 [0, 0, 0, 0, S, 0],
				 [0, 0, 0, V, 0, 0],
				 [0, 0, S, 0, 0, 0],
				 [V, S, S, S, V, 0],
				 [V, 0, 0, 0, 0, 0]])
s3_d = np.array([[V, 0, 0, 0, 0, 0, 0, 0],
				 [0, S, 0, 0, 0, 0, 0, V],
				 [0, 0, V, 0, 0, 0, S, 0],
				 [0, 0, 0, S, 0, S, 0, 0],
				 [0, 0, 0, 0, S, 0, 0, 0],
				 [0, 0, 0, V, 0, V, 0, 0]])

s4_a = np.array([[V, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, S, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, S, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, V, 0, 0, 0, 0, 0],
                 [0, 0, 0, V, S, V, S, S, V],
                 [0, 0, 0, 0, 0, V, 0, 0, 0]])
s4_b = np.array([[0, V, 0, 0, 0, 0],
                 [0, S, 0, 0, 0, 0],
                 [0, S, 0, 0, 0, 0],
                 [0, V, 0, 0, 0, 0],
                 [V, S, V, S, S, V],
                 [0, V, 0, 0, 0, 0]])
s4_c = np.array([[0, 0, 0, 0, 0, V],
                 [0, 0, 0, 0, S, 0],
                 [0, 0, 0, S, 0, 0],
                 [0, 0, V, 0, 0, 0],
                 [V, S, V, S, S, V],
                 [V, 0, 0, 0, 0, 0]])
s4_d = np.array([[V, 0, 0, 0, 0, 0, 0, 0, V],
                 [0, S, 0, 0, 0, 0, 0, S, 0],
                 [0, 0, S, 0, 0, 0, S, 0, 0],
                 [0, 0, 0, V, 0, V, 0, 0, 0],
                 [0, 0, 0, 0, S, 0, 0, 0, 0],
                 [0, 0, 0, V, 0, V, 0, 0, 0]])

s5_a = np.array([[V, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, S, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, S, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, V, 0, 0, 0, 0, 0],
                 [0, 0, 0, V, S, S, V, S, V],
                 [0, 0, 0, 0, 0, V, 0, 0, 0]])
s5_b = np.array([[0, V, 0, 0, 0, 0],
                 [0, S, 0, 0, 0, 0],
                 [0, S, 0, 0, 0, 0],
                 [0, V, 0, 0, 0, 0],
                 [V, S, S, V, S, V],
                 [0, V, 0, 0, 0, 0]])
s5_c = np.array([[0, 0, 0, 0, 0, V],
                 [0, 0, 0, 0, S, 0],
                 [0, 0, 0, S, 0, 0],
                 [0, 0, V, 0, 0, 0],
                 [V, S, S, V, S, V],
                 [V, 0, 0, 0, 0, 0]])
s5_d = np.array([[V, 0, 0, 0, 0, 0, 0, 0, V],
                 [0, S, 0, 0, 0, 0, 0, S, 0],
                 [0, 0, S, 0, 0, 0, V, 0, 0],
                 [0, 0, 0, V, 0, S, 0, 0, 0],
                 [0, 0, 0, 0, S, 0, 0, 0, 0],
                 [0, 0, 0, V, 0, V, 0, 0, 0]])

s6_a = np.array([[V, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, S, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, V, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, S, 0, 0, 0, 0, 0],
                 [0, 0, 0, V, S, S, V, S, V],
                 [0, 0, 0, 0, 0, V, 0, 0, 0]])
s6_b = np.array([[0, V, 0, 0, 0, 0],
                 [0, S, 0, 0, 0, 0],
                 [0, V, 0, 0, 0, 0],
                 [0, S, 0, 0, 0, 0],
                 [V, S, S, V, S, V],
                 [0, V, 0, 0, 0, 0]])
s6_c = np.array([[0, 0, 0, 0, 0, V],
                 [0, 0, 0, 0, S, 0],
                 [0, 0, 0, V, 0, 0],
                 [0, 0, S, 0, 0, 0],
                 [V, S, S, V, S, V],
                 [V, 0, 0, 0, 0, 0]])
s6_d = np.array([[V, 0, 0, 0, 0, 0, 0, 0, V],
                 [0, S, 0, 0, 0, 0, 0, S, 0],
                 [0, 0, V, 0, 0, 0, V, 0, 0],
                 [0, 0, 0, S, 0, S, 0, 0, 0],
                 [0, 0, 0, 0, S, 0, 0, 0, 0],
                 [0, 0, 0, V, 0, V, 0, 0, 0]])
