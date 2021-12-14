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

# =========================================================================== #
#                          | functions definition |                           #
# =========================================================================== #

def remove_opponent_pair(grid:np.array, last_coord:np.array, idx:int):
    yx = last_coord
    #explicite coordinates of the stone to remove along each possible direction
    # from the stone just played
    stone_to_del = ((yx[0] + np.array([-2, -1]), yx[1] + np.array([0, 0])),
                    (yx[0] + np.array([1, 2]), yx[1] + np.array([0, 0])),
                    (yx[0] + np.array([0, 0]), yx[1] + np.array([-2, -1])),
                    (yx[0] + np.array([0, 0]), yx[1] + np.array([1, 2])),
                    (yx[0] + np.array([-2, -1]), yx[1] + np.array([-2, -1])),
                    (yx[0] + np.array([-2, -1]), yx[1] + np.array([2, 1])),
                    (yx[0] + np.array([2, 1]), yx[1] + np.array([-2, -1])),
                    (yx[0] + np.array([1, 2]), yx[1] + np.array([1, 2])))
    grid[stone_to_del[idx]] = 0


def iscapture_position(grid:np.array, last_coord:np.array, color:int) -> bool:
    """[summary]
    Args:
        yx ([type]): [description]
        grid ([type]): [description]
    Returns:
        bool: [description]
    """
    yx = last_coord
    c = color
    
    pad_width = 3
    extend_grid = np.pad(grid, (pad_width), "constant", constant_values = (0))
    extend_grid[yx[0] + pad_width, yx[1] + pad_width] = c
    
    r_conv_c1 = np.sum(np.multiply(extend_grid[yx[0]:yx[0] + 4, yx[1] + 3:yx[1] + 4], c * k_captures['column']))
    r_conv_c2 = np.sum(np.multiply(extend_grid[yx[0] + 3:yx[0] + 7, yx[1] + 3:yx[1] + 4], c * k_captures['column']))
    
    r_conv_l1 = np.sum(np.multiply(extend_grid[yx[0] + 3:yx[0]+4, yx[1]:yx[1] + 4], c * k_captures['line']))
    r_conv_l2 = np.sum(np.multiply(extend_grid[yx[0] + 3:yx[0]+4, yx[1] + 3:yx[1] + 7], c * k_captures['line']))
    
    r_conv_d1 = np.sum(np.multiply(extend_grid[yx[0]:yx[0] + 4, yx[1]:yx[1] + 4], c * k_captures['diag1']))
    r_conv_d2 = np.sum(np.multiply(extend_grid[yx[0]:yx[0] + 4, yx[1] + 3:yx[1] + 7], c * k_captures['diag2']))
    r_conv_d3 = np.sum(np.multiply(extend_grid[yx[0] + 3:yx[0] + 7, yx[1]:yx[1] + 4], c * k_captures['diag2']))
    r_conv_d4 = np.sum(np.multiply(extend_grid[yx[0] + 3:yx[0] + 7, yx[1] + 3:yx[1] + 7], c * k_captures['diag1']))
    res = [r_conv_c1, r_conv_c2, r_conv_l1, r_conv_l2, r_conv_d1, r_conv_d2, r_conv_d3, r_conv_d4]
    
    for ii, r_conv in enumerate(res):
        if (r_conv == 4):
            remove_opponent_pair(grid, yx, ii)
    if any([r == 4 for r in res]):
        return True
    return False