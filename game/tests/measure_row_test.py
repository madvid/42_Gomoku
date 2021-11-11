from board import *

def test_row1():
    g = np.array([
        [1, 0, 0],
        [1, 0, 0],
        [1, 1, 0]
        ])
    print(g)    
    assert measure_row(g, 1) == 2

def test_row2():
    g = np.array([
        [1, 0, 0],
        [1, 0, 0],
        [1, 1, 1]
        ])
    print(g)    
    assert measure_row(g, 1) == 3

def test_row3():
    g = np.array([
        [1, 0, 0],
        [1, 0, 0],
        [1, 0, 1]
        ])
    print(g)    
    assert measure_row(g, 1) == 1


def test_row4():
    g = np.array([
        [0, 1, 1],
        [1, 0, 0],
        [1, 0, 0]
        ])
    print(g)    
    assert measure_row(g, 1) == 2

def test_row5():
    g = np.array([
        [1, 0, 0],
        [1, 0, 0],
        [0, 0, 1]
        ])
    print(g)    
    assert measure_row(g, 1) == 1