import numpy as np
from typing import List, Tuple
from game.metrics import get_kern_row_idx, get_kern_col_idx, get_kern_diag_idx

# =========================================================================== #
#                          | constants definition |                           #
# =========================================================================== #

k_capture = np.array([1, -1, -1, 1])

# =========================================================================== #
#                          | functions definition |                           #
# =========================================================================== #

def remove_opponent_pair(grid:np.array, coords_lst):
    for pair in coords_lst:
        grid[pair] = 0


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
    
    r_conv_c1 = np.dot(grid[get_kern_col_idx(yx, direction=-1, length=4)], color * k_capture)
    r_conv_c2 = np.dot(grid[get_kern_col_idx(yx, direction=1, length=4)], color * k_capture) # FIXME: identical to the line above
    
    r_conv_l1 = np.dot(grid[get_kern_row_idx(yx, direction=-1, length=4)], color * k_capture)
    r_conv_l2 = np.dot(grid[get_kern_row_idx(yx, direction=1, length=4)], color * k_capture) # FIXME: identical to the line above
    
    r_conv_d1 = np.dot(grid[get_kern_diag_idx(yx, (-1, -1), 4)], color * k_capture)
    r_conv_d2 = np.dot(grid[get_kern_diag_idx(yx, (-1, 1), 4)], color * k_capture) # FIXME: identical to the line above
    r_conv_d3 = np.dot(grid[get_kern_diag_idx(yx, (1, -1), 4)], color * k_capture) # FIXME: identical to the line above
    r_conv_d4 = np.dot(grid[get_kern_diag_idx(yx, (1, 1), 4)], color * k_capture) # FIXME: identical to the line above
    
    res = [r_conv_c1, r_conv_c2, r_conv_l1, r_conv_l2, r_conv_d1, r_conv_d2, r_conv_d3, r_conv_d4]
    return [pair_to_del[ii] for ii, r_conv in enumerate(res) if r_conv == 4]