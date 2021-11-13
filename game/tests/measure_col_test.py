from metrics import *

def test_col1():
    g = np.array([
        [1, 1, 1],
        [1, 0, 0],
        [0, 0, 0]
        ])
    assert measure_col(g, 1) == [Column(2, Position(0,0), 1, g)]

def test_col2():
    g = np.array([
        [1, 0, 0],
        [1, 0, 0],
        [1, 1, 1]
        ])
    assert measure_col(g, 1) == [Column(3, Position(0,0), 1, g)]

def test_col3():
    g = np.array([
        [1, 0, 0],
        [0, 0, 1],
        [1, 0, 1]
        ])
    assert measure_col(g, 1) == [Column(2, Position(1,2), 1, g)]

def test_col4():
    g = np.array([
        [0, 1, 1],
        [1, 1, 1],
        [1, 1, 0]
        ])
    assert measure_col(g, 1) == [Column(2, Position(1,0), 1, g), Column(3, Position(0,1), 1, g), Column(2, Position(0,2), 1, g)]

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

def test_col7():
    g = np.array([
        [0, 0, 1, 0, 1],
        [0, 0, 0, 0, 1],
        [1, 1, 0, 0, 0],
        [0, 0, 0, 0, 1],
        [1, 1, 1, 0, 1],
        ])
    assert measure_col(g, 1) == [Column(2, Position(0, 4), 1, g), Column(2, Position(3,4), 1, g)]

def test_col8():
    g = np.array([
        [0, 1, 1, 0, 0],
        [0, 0, 0, 0, 0],
        [1, 1, 0, 0, 0],
        [0, 1, 0, 0, 0],
        [1, 1, 1, 0, 0],
        ])
    assert measure_col(g, 1) == [Column(3, Position(2, 1), 1, g)]


def test_col9():
    g = np.array([
        [0, 0, 1, 0, 0],
        [0, 1, 0, 0, 0],
        [1, 1, 0, 0, 0],
        [0, 1, 0, 0, 0],
        [1, 0, 1, 0, 0],
        ])
    assert measure_col(g, 1) == [Column(3, Position(1, 1), 1, g)]

def test_col10():
    g = np.array([
        [0, 0, 1, 1, 1],
        [0, 1, 1, 0, 1],
        [1, 1, 1, 1, 0],
        [0, 1, 0, 1, 1],
        [1, 0, 1, 1, 1],
        ])
    assert measure_col(g, 1) == [Column(3, Position(1,1), 1, g), Column(3, Position(0,2), 1, g), Column(3, Position(2,3), 1, g), 
                                 Column(2, Position(0,4), 1, g), Column(2, Position(3,4), 1, g)]
