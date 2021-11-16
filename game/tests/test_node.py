import numpy as np
from board import *

def test_update():
    g = np.array([
        [1, 0, 0],
        [0, 0, 1],
        [1, 0, 1]
        ])
    node = Node(None, g, 1)
    update_node = node.update((1,1), -1)
    expected_res = np.array([
                    [1,  0, 0],
                    [0, -1, 1],
                    [1,  0, 1]
                    ])

    assert (update_node.grid == expected_res).all()

def test_generate_next_moves():
    g = np.array([
        [1, 1, 0],
        [0, 1, 1],
        [1, 1, 1]
        ])
    node = Node(None, g, 1)
    next_moves = [n.grid for n in node.generate_next_moves()]

    expected_res = [np.array([
                        [1, 1, -1],
                        [0, 1, 1],
                        [1, 1, 1]
                        ]), 
                        np.array([
                        [1, 1, 0],
                        [-1, 1, 1],
                        [1, 1, 1]
                        ]
                        )]

    assert (expected_res[0] == next_moves[0]).all()
    assert (expected_res[1] == next_moves[1]).all()