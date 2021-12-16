import numpy as np
from typing import List, Tuple
from game.metrics import get_kern_row_idx, get_kern_col_idx, get_kern_diag_idx

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

k_capture = np.array([BLACK, WHITE, WHITE, BLACK])

# =========================================================================== #
#                          | functions definition |                           #
# =========================================================================== #

def _DEPRECATED_remove_opponent_pair(grid:np.array, last_coord:np.array, idx:int):
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

def remove_opponent_pair(grid:np.array, coords_lst):
    for pair in coords_lst:
        grid[pair] = 0


def _DEPRECATED_iscapture_position(grid:np.array, last_coord:np.array, color:int) -> bool:
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


def iscapture_position(grid:np.array, current_pos:np.array, color:int) -> List[Tuple[np.ndarray]]: # FIXME: create a understandable POSITION type alias 
    """[summary]
    Args:
        yx ([type]): [description]
        grid ([type]): [description]
    Returns:
        bool: [description]
    """
    yx = current_pos
    pair_to_del = ((yx[0] + np.array([-2, -1]), yx[1] + np.array([0, 0])),
                   (yx[0] + np.array([1, 2]), yx[1] + np.array([0, 0])),
                   (yx[0] + np.array([0, 0]), yx[1] + np.array([-2, -1])),
                   (yx[0] + np.array([0, 0]), yx[1] + np.array([1, 2])),
                   (yx[0] + np.array([-2, -1]), yx[1] + np.array([-2, -1])),
                   (yx[0] + np.array([-2, -1]), yx[1] + np.array([2, 1])),
                   (yx[0] + np.array([2, 1]), yx[1] + np.array([-2, -1])),
                   (yx[0] + np.array([1, 2]), yx[1] + np.array([1, 2])))
    
    # FIXME: use np.convolve instead
    r_conv_c1 = np.sum(np.multiply(grid[get_kern_col_idx(yx)], color * k_capture))
    r_conv_c2 = np.sum(np.multiply(grid[get_kern_col_idx(yx)], color * k_capture))
    
    r_conv_l1 = np.sum(np.multiply(grid[get_kern_row_idx(yx)], color * k_capture))
    r_conv_l2 = np.sum(np.multiply(grid[get_kern_row_idx(yx)], color * k_capture))
    
    r_conv_d1 = np.sum(np.multiply(grid[get_kern_diag_idx(yx)], color * k_capture))
    r_conv_d2 = np.sum(np.multiply(grid[get_kern_diag_idx(yx)], color * k_capture))
    r_conv_d3 = np.sum(np.multiply(grid[get_kern_diag_idx(yx)], color * k_capture))
    r_conv_d4 = np.sum(np.multiply(grid[get_kern_diag_idx(yx)], color * k_capture))
    res = [r_conv_c1, r_conv_c2, r_conv_l1, r_conv_l2, r_conv_d1, r_conv_d2, r_conv_d3, r_conv_d4]
    
    return [pair_to_del[ii] for ii, r_conv in enumerate(res) if r_conv == 4]