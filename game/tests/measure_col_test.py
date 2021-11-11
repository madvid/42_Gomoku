from metrics import *

def test_row1():
    g = np.array([
        [1, 0, 0],
        [1, 0, 0],
        [1, 1, 0]
        ])
    assert measure_col(g, 1) == 3

def test_row2():
    g = np.array([
        [1, 0, 0],
        [0, 0, 0],
        [1, 1, 1]
        ])
    assert measure_col(g, 1) == 1

def test_row3():
    g = np.array([
        [1, 0, 0],
        [0, 0, 1],
        [1, 0, 1]
        ])
    assert measure_col(g, 1) == 2


def test_row4():
    g = np.array([
        [0, 1, 1],
        [1, 0, 0],
        [1, 0, 0]
        ])
    assert measure_col(g, 1) == 2

def test_row5():
    g = np.array([
        [1, 0, 0],
        [1, 0, 0],
        [0, 0, 1]
        ])
    assert measure_col(g, 1) == 2