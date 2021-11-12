from metrics import *

def test_diag1():
    g = np.array([
        [0, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [1, 0, 0, 0]
        ])
    assert measure_diag(g, 1) == [Diagonal(2, (1, 1), True)]

def test_diag2():
    g = np.array([
        [0, 0, 0, 0],
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0]
        ])
    assert measure_diag(g, 1) == [Diagonal(3, (1, 0), True)]

def test_diag3():
    g = np.array([
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [1, 0, 0, 1],
        [0, 1, 0, 0]
        ])
    assert measure_diag(g, 1) == [Diagonal(2, (2, 0), True), Diagonal(3, (0,1), True)]

def test_diag4():
    g = np.array([
        [0, 1, 0, 1],
        [0, 0, 1, 0],
        [1, 1, 0, 1],
        [0, 1, 0, 0]
        ])
    assert measure_diag(g, 1) == [
                                Diagonal(2, (2, 0), True), 
                                Diagonal(3, (0,1), True),
                                Diagonal(3, (0,3), False)]

def test_diag5():
    g = np.array([
        [0, 0, 0, 0],
        [1, 0, 1, 0],
        [0, 1, 0, 1],
        [1, 0, 0, 0]
        ])
    assert measure_diag(g, 1) == [Diagonal(2, (1, 0), True), Diagonal(2, (1, 2), True),
                                  Diagonal(3, (1, 2), False)]