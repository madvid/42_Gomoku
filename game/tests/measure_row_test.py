from metrics import *

def test_row1():
    g = np.array([
        [1, 0, 0],
        [1, 0, 0],
        [1, 1, 0]
        ])
    assert measure_row(g, 1) == [Row(2, (2,0))]

def test_row2():
    g = np.array([
        [1, 0, 0],
        [1, 0, 0],
        [1, 1, 1]
        ])
    assert measure_row(g, 1) == [Row(3, (2,0))]

def test_row3():
    g = np.array([
        [1, 0, 0],
        [1, 0, 0],
        [0, 1, 1]
        ])
    assert measure_row(g, 1) == [Row(2, (2,1))]

def test_row4():
    g = np.array([
        [0, 1, 1],
        [1, 1, 0],
        [1, 1, 1]
        ])
    assert measure_row(g, 1) == [Row(2, (0, 1)), Row(2, (1, 0)), Row(3, (2,0))]

def test_row5():
    g = np.array([
        [0, 1, 0],
        [1, 0, 1],
        [0, 1, 0]
        ])
    assert measure_row(g, 1) == []

def test_row6():
    g = np.array([
        [0, 0, 1],
        [1, 0, 1],
        [0, 0, 1]
        ])
    assert measure_row(g, 1) == []

def test_row7():
    g = np.array([
        [0, 0, 1, 0, 1],
        [0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1],
        [1, 1, 0, 1, 1],
        ])
    assert measure_row(g, 1) == [Row(2, (4, 0)), Row(2, (4,3))]

def test_row8():
    g = np.array([
        [0, 1, 0, 0, 0],
        [1, 0, 1, 1, 1],
        [1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0],
        [1, 0, 0, 0, 0],
        ])
    assert measure_row(g, 1) == [Row(3, (1, 2))] #, Row(2, (0, 4)), Row(2, (3,4))]