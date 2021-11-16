from metrics import *

def test_row1():
    g = np.array([
        [0,  0,  0,  0,  0, 0],
        [0,  1,  1,  0,  1, 0],
        [1,  0,  0,  0,  0, 0],
        [0,  0,  0,  0,  1, 0],
        [1,  1,  0,  1,  1, 0],
        [1,  1,  0,  1,  1, 0]
        ])
    row = Row(2, Position(1,1), 1, g)
    assert row.is_a_bridge()

def test_row2():
    g = np.array([
        [0,  0,  0,  0,  0, 0],
        [0,  1,  0,  1,  1, 0],
        [1,  0,  0,  0,  0, 0],
        [0,  0,  0,  0,  1, 0],
        [1,  1,  0,  1,  1, 0],
        [1,  1,  0,  1,  1, 0]
        ])
    row = Row(2, Position(1,3), 1, g)
    assert row.is_a_bridge()

def test_row3():
    g = np.array([
        [0,  0,  0,  0,  0,  0],
        [0,  1, -1,  1,  1,  0],
        [1,  0,  0,  0,  0,  0],
        [0,  0,  0,  0,  1,  0],
        [1,  1,  0,  1,  1,  0],
        [1,  1,  0,  1,  1,  0]
        ])
    row = Row(2, Position(1,3), 1, g)
    assert not row.is_a_bridge()

def test_row4():
    g = np.array([
        [0,  0,  0,  0,  0, 0],
        [0,  1,  1, -1,  1, 0],
        [1,  0,  0,  0,  0, 0],
        [0,  0,  0,  0,  1, 0],
        [1,  1,  0,  1,  1, 0],
        [1,  1,  0,  1,  1, 0]
        ])
    row = Row(2, Position(1,1), 1, g)
    assert not row.is_a_bridge()

def test_row5():
    g = np.array([
        [0,  0,  0,  0,  0, 0],
        [-1, 1,  1,  0,  1, 0],
        [1,  0,  0,  0,  0, 0],
        [0,  0,  0,  0,  1, 0],
        [1,  1,  0,  1,  1, 0],
        [1,  1,  0,  1,  1, 0]
        ])
    row = Row(2, Position(1,1), 1, g)
    assert not row.is_a_bridge()

def test_row6():
    g = np.array([
        [0,  0,  0,  0,  0,  0],
        [0,  1,  1,  0,  1, -1],
        [1,  0,  0,  0,  0,  0],
        [0,  0,  0,  0,  1,  0],
        [1,  1,  0,  1,  1,  0],
        [1,  1,  0,  1,  1,  0]
        ])
    row = Row(2, Position(1,1), 1, g)
    assert not row.is_a_bridge()

def test_col1():
    g = np.array([
        [0,  0,  0,  0,  0, 0],
        [0,  1,  1,  1,  0, 0],
        [1,  0,  1,  0,  0, 0],
        [0,  0,  0,  0,  1, 0],
        [1,  1,  1,  1,  1, 0],
        [1,  1,  0,  1,  1, 0]
        ])
    col = Column(2, Position(1,2), 1, g)
    assert col.is_a_bridge()

def test_col2():
    g = np.array([
        [0,  0,  0,  0,  0, 0],
        [0,  1,  1,  1,  0, 0],
        [1,  0,  0,  0,  0, 0],
        [0,  0,  1,  0,  1, 0],
        [1,  1,  1,  1,  1, 0],
        [1,  1,  0,  1,  1, 0]
        ])
    col = Column(2, Position(3,2), 1, g)
    assert col.is_a_bridge()

def test_col3():
    g = np.array([
        [0,  0,  0,  0,  0, 0],
        [0,  1,  1,  1,  0, 0],
        [1,  0,  1,  0,  0, 0],
        [0,  0, -1,  0,  1, 0],
        [1,  1,  1,  1,  1, 0],
        [1,  1,  0,  1,  1, 0]
        ])
    col = Column(2, Position(1,2), 1, g)
    assert not col.is_a_bridge()


def test_col4():
    g = np.array([
        [0,  0,  0,  0,  0, 0],
        [0,  1,  1,  1,  0, 0],
        [1,  0, -1,  0,  0, 0],
        [0,  0,  1,  0,  1, 0],
        [1,  1,  1,  1,  1, 0],
        [1,  1,  0,  1,  1, 0]
        ])
    col = Column(2, Position(3,2), 1, g)
    assert not col.is_a_bridge()


def test_col5():
    g = np.array([
        [0,  0,  0,  0,  0, 0],
        [0,  1,  1,  1,  0, 0],
        [1,  0,  0,  0,  0, 0],
        [0,  0,  1,  0,  1, 0],
        [1,  1,  1,  1,  1, 0],
        [1,  1, -1,  1,  1, 0]
        ])
    col = Column(2, Position(3,2), 1, g)
    assert not col.is_a_bridge()

def test_col6():
    g = np.array([
        [0,  0, -1,  0,  0, 0],
        [0,  1,  1,  1,  0, 0],
        [1,  0,  0,  0,  0, 0],
        [0,  0,  1,  0,  1, 0],
        [1,  1,  1,  1,  1, 0],
        [1,  1,  0,  1,  1, 0]
        ])
    col = Column(2, Position(3,2), 1, g)
    assert not col.is_a_bridge()

def test_diag1():
    g = np.array([
        [0,  0,  0,  0,  0, 0],
        [0,  1,  1,  1,  0, 0],
        [1,  0,  0,  0,  0, 0],
        [0,  0,  1,  1,  1, 0],
        [1,  1,  0,  1,  1, 0],
        [1,  1,  0,  1,  1, 0]
        ])
    diag = Diagonal(2, Position(3,3), 1, g, True)
    assert diag.is_a_bridge()

def test_diag2():
    g = np.array([
        [0,  0,  0,  0,  0, 0],
        [0,  1,  1,  1,  0, 0],
        [1,  0,  1,  0,  0, 0],
        [0,  0,  1,  0,  1, 0],
        [1,  1,  0,  1,  1, 0],
        [1,  1,  0,  1,  1, 0]
        ])
    diag = Diagonal(2, Position(1,1), 1, g, True)
    assert diag.is_a_bridge()

def test_diag3():
    g = np.array([
        [0,  0,  0,  0,  0, 0],
        [0,  1,  1,  1,  0, 0],
        [1,  0, -1,  0,  0, 0],
        [0,  0,  1,  1,  1, 0],
        [1,  1,  0,  1,  1, 0],
        [1,  1,  0,  1,  1, 0]
        ])
    diag = Diagonal(2, Position(3,3), 1, g, True)
    assert not diag.is_a_bridge()


def test_diag4():
    g = np.array([
        [0,  0,  0,  0,  0, 0],
        [0,  1,  1,  1,  0, 0],
        [1,  0,  1,  0,  0, 0],
        [0,  0,  1, -1,  1, 0],
        [1,  1,  0,  1,  1, 0],
        [1,  1,  0,  1,  1, 0]
        ])
    diag = Diagonal(2, Position(1,1), 1, g, True)
    assert not diag.is_a_bridge()

def test_diag5():
    g = np.array([
        [-1, 0,  0,  0,  0, 0],
        [0,  1,  1,  1,  0, 0],
        [1,  0,  1,  0,  0, 0],
        [0,  0,  1,  0,  1, 0],
        [1,  1,  0,  1,  1, 0],
        [1,  1,  0,  1,  1, 0]
        ])
    diag = Diagonal(2, Position(1,1), 1, g, True)
    assert not diag.is_a_bridge()

def test_diag6():
    g = np.array([
        [0, 0,  0,  0,   0,  0],
        [0,  1,  1,  1,  0,  0],
        [1,  0,  1,  0,  0,  0],
        [0,  0,  1,  0,  1,  0],
        [1,  1,  0,  1,  1,  0],
        [1,  1,  0,  1,  1, -1]
        ])
    diag = Diagonal(2, Position(1,1), 1, g, True)
    assert not diag.is_a_bridge()

def test_rdiag1():
    g = np.array([
        [0,  0,  0,  0,  0, 0],
        [0,  1,  1,  1,  1, 0],
        [1,  0,  1,  1,  0, 0],
        [0,  0,  0,  1,  1, 0],
        [1,  1,  0,  1,  0, 0],
        [0,  1,  0,  1,  1, 0]
        ])
    diag = Diagonal(2, Position(1,4), 1, g, False)
    assert diag.is_a_bridge()

def test_rdiag2():
    g = np.array([
        [0,  0,  0,  0,  0, 0],
        [0,  1,  1,  1,  1, 0],
        [1,  0,  1,  0,  0, 0],
        [0,  0,  1,  1,  1, 0],
        [1,  1,  0,  1,  0, 0],
        [0,  1,  0,  1,  1, 0]
        ])
    diag = Diagonal(2, Position(3,2), 1, g, False)
    assert diag.is_a_bridge()

def test_rdiag3():
    g = np.array([
        [0,  0,  0,  0,  0, 0],
        [0,  1,  1,  1,  1, 0],
        [1,  0,  1,  1,  0, 0],
        [0,  0, -1,  1,  1, 0],
        [1,  1,  0,  1,  0, 0],
        [0,  1,  0,  1,  1, 0]
        ])
    diag = Diagonal(2, Position(1,4), 1, g, False)
    assert not diag.is_a_bridge()


def test_rdiag4():
    g = np.array([
        [0,  0,  0,  0,  0, 0],
        [0,  1,  1,  1,  1, 0],
        [1,  0,  1, -1,  0, 0],
        [0,  0,  1,  1,  1, 0],
        [1,  1,  0,  1,  0, 0],
        [0,  1,  0,  1,  1, 0]
        ])
    diag = Diagonal(2, Position(3,2), 1, g, False)
    assert not diag.is_a_bridge()


def test_rdiag5():
    g = np.array([
        [0,  0,  0,  0,  0, -1],
        [0,  1,  1,  1,  1,  0],
        [1,  0,  1,  0,  0,  0],
        [0,  0,  1,  1,  1,  0],
        [1,  1,  0,  1,  0,  0],
        [0,  1,  0,  1,  1,  0]
        ])
    diag = Diagonal(2, Position(3,2), 1, g, False)
    assert not diag.is_a_bridge()

def test_rdiag6():
    g = np.array([
        [0,  0,  0,  0,  0,  0],
        [0,  1,  1,  1,  1,  0],
        [1,  0,  1,  0,  0,  0],
        [0,  0,  1,  1,  1,  0],
        [1,  1,  0,  1,  0,  0],
        [-1, 1,  0,  1,  1,  0]
        ])
    diag = Diagonal(2, Position(3,2), 1, g, False)
    assert not diag.is_a_bridge()