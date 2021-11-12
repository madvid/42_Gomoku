from metrics import *

def test_col1():
    g = np.array([
        [1, 1, 1],
        [1, 0, 0],
        [0, 0, 0]
        ])
    assert measure_col(g, 1) == [Column(2, (0,0))]

def test_col2():
    g = np.array([
        [1, 0, 0],
        [1, 0, 0],
        [1, 1, 1]
        ])
    assert measure_col(g, 1) == [Column(3, (0,0))]

def test_col3():
    g = np.array([
        [1, 0, 0],
        [0, 0, 1],
        [1, 0, 1]
        ])
    assert measure_col(g, 1) == [Column(2, (1,2))]


def test_col4():
    g = np.array([
        [0, 1, 1],
        [1, 1, 1],
        [1, 1, 0]
        ])
    assert measure_col(g, 1) == [Column(2, (1,0)), Column(3, (0,1)), Column(2, (0,2))]

def test_col5():
    g = np.array([
        [0, 1, 0],
        [1, 0, 1],
        [0, 1, 0]
        ])
    assert measure_col(g, 1) == []

def test_col6():
    g = np.array([
        [0, 0, 1],
        [0, 0, 0],
        [1, 1, 1]
        ])
    assert measure_col(g, 1) == []