from board import Node
from metrics import  *

def test_node1():
    g = np.array([
        [1, -1, -1],
        [1, -1, -1],
        [1,  1,  0]
        ])
    n = Node(None, g, BLACK)
    next_mv = n.generate_next_moves()
    assert (next_mv[0].grid == np.array([
        [1, -1, -1],
        [1, -1, -1],
        [1,  1, -1]
        ])).all()
    assert next_mv[0].color == WHITE

def test_node2():
    g = np.array([
        [0, -1, -1],
        [1, -1, -1],
        [1,  1,  1]
        ])
    n = Node(None, g, BLACK)
    next_mv = n.generate_next_moves()
    assert (next_mv[0].grid == np.array([
        [-1, -1, -1],
        [1,  -1, -1],
        [1,   1,  1]
        ])).all()
    assert next_mv[0].color == WHITE

def test_row1():
    g = np.array([
        [1,  1,  1,  1],
        [1,  1,  1,  1],
        [1, -1, -1,  0],
        [1,  1,  1,  1],
        [1,  1,  1,  1]
        ])
    n = Node(None, g, WHITE)
    next_mv = n.generate_next_moves()
    assert (next_mv[0].grid == np.array([
        [1,  1,  1,  1],
        [1,  1,  1,  1],
        [1,  0,  0,  1],
        [1,  1,  1,  1],
        [1,  1,  1,  1]
        ])).all()

def test_col1():
    g = np.array([
        [1,  0,  1,  1],
        [1, -1,  1,  1],
        [1, -1,  1,  1],
        [1,  1,  1,  1],
        [1,  1,  1,  1]
        ])
    n = Node(None, g, WHITE)
    next_mv = n.generate_next_moves()
    assert (next_mv[0].grid == np.array([
        [1,  1,  1,  1],
        [1,  0,  1,  1],
        [1,  0,  1,  1],
        [1,  1,  1,  1],
        [1,  1,  1,  1]
        ])).all()

def test_diag1():
    g = np.array([
        [1,  1,  1,  1],
        [1, -1,  1,  1],
        [1,  1, -1,  1],
        [1,  1,  1,  0],
        [1,  1,  1,  1]
        ])
    n = Node(None, g, WHITE)
    next_mv = n.generate_next_moves()
    assert (next_mv[0].grid == np.array([
        [1,  1,  1,  1],
        [1,  0,  1,  1],
        [1,  1,  0,  1],
        [1,  1,  1,  1],
        [1,  1,  1,  1]
        ])).all()


def test_diag2():
    g = np.array([
        [0,  1,  1,  1],
        [1, -1,  1,  1],
        [1,  1, -1,  1],
        [1,  1,  1,  1]
        ])
    n = Node(None, g, WHITE)
    next_mv = n.generate_next_moves()
    assert (next_mv[0].grid == np.array([
        [1,  1,  1,  1],
        [1,  0,  1,  1],
        [1,  1,  0,  1],
        [1,  1,  1,  1]
        ])).all()

def test_rdiag1():
    g = np.array([
        [1,  1,  1,  1, 1],
        [1,  1,  1,  0, 1],
        [1,  1, -1,  1, 1],
        [1, -1,  1,  1, 1],
        [1,  1,  1,  1, 1]
        ])
    n = Node(None, g, WHITE)
    next_mv = n.generate_next_moves()
    assert (next_mv[0].grid == np.array([
        [1,  1,  1,  1, 1],
        [1,  1,  1,  1, 1],
        [1,  1,  0,  1, 1],
        [1,  0,  1,  1, 1],
        [1,  1,  1,  1, 1]
        ])).all()