from metrics import *

def test_diag1():
    g = np.array([
        [0, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [1, 0, 0, 0]
        ])
    assert measure_diag(g, 1) == [Diagonal(2, Position(1, 1), 1, g, True)]

def test_diag2():
    g = np.array([
        [0, 0, 0, 0],
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0]
        ])
    assert measure_diag(g, 1) == [Diagonal(3, Position(1, 0), 1, g, True)]

def test_diag3():
    g = np.array([
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [1, 0, 0, 1],
        [0, 1, 0, 0]
        ])
    assert measure_diag(g, 1) == [Diagonal(2, Position(2, 0), 1, g, True), Diagonal(3, Position(0,1), 1, g, True)]

def test_diag4():
    g = np.array([
        [0, 1, 0, 1],
        [0, 0, 1, 0],
        [1, 1, 0, 1],
        [0, 1, 0, 0]
        ])
    assert measure_diag(g, 1) == [
                                Diagonal(2, Position(2, 0), 1, g, True), 
                                Diagonal(3, Position(0,1), 1, g, True),
                                Diagonal(3, Position(0,3), 1, g, False)]

def test_diag5():
    g = np.array([
        [0, 0, 0, 0],
        [1, 0, 1, 0],
        [0, 1, 0, 1],
        [1, 0, 0, 0]
        ])
    assert measure_diag(g, 1) == [Diagonal(2, Position(1, 0), 1, g, True), Diagonal(2, Position(1, 2), 1, g, True),
                                  Diagonal(3, Position(1, 2), 1, g, False)]