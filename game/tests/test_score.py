# from metrics import *
from game.board import Node
import numpy as np

def test_row_black1():
    g = np.array([
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 1,-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0,-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    )
    parent = Node(None, np.pad(g, 4, 'constant', constant_values=0), -1, pos = (4,4))

    color = -1
    node = Node(parent, np.pad(g, 4, 'constant', constant_values=0), color, pos = (5,5))
    assert node.score(-1) == 2

# def test_row_black2():
#     g = np.array([
#         [0,  0,  0,  0,  0, 0],
#         [0,  1,  1,  1,  0, 0],
#         [0, -1, -1, -1, -1, 0],
#         [0,  0,  0,  0,  0, 0],
#         [0,  0,  0,  0,  0, 0],
#         [0,  0,  0,  0,  0, 0]
#         ])
#     assert collect_sequences(g, 1) == 3

# def test_row_black3():
#     g = np.array([
#         [0,  0,  0,  0,  0, 0],
#         [0,  1,  1,  1,  0, 0],
#         [0,  0,  0,  0,  0, 0],
#         [0,  0,  0, -1,  0, 0],
#         [0,  0,  0, -1,  0, 0],
#         [0,  0,  0,  0,  0, 0]
#         ])
#     assert collect_sequences(g, 1) == 3

# def test_row_black4():
#     g = np.array([
#         [0,  0,  0,  0,  0,-1],
#         [0,  1,  1,  0,  0, 0],
#         [0,  0,  1, -1,  0, 0],
#         [0,  0, -1,  1,  0, 0],
#         [0, -1,  0,  0,  1, 0],
#         [0,  0,  0,  0,  0, 0]
#         ])
#     assert collect_sequences(g, 1) == 4

# def test_row_black5():
#     g = np.array([
#         [0,  0,  0,  0,  0, -1],
#         [0, -1,  1,  0,  0, 0],
#         [0,  0, -1,  1,  0, 0],
#         [0,  0,  1, -1,  0, 0],
#         [0,  1,  0,  0, -1, 0],
#         [0,  0,  0,  0,  0, 0]
#         ])
#     assert collect_sequences(g, 1) == 3

# def test_row_white1():
#     g = np.array([
#         [0,  0,  0,  0,  0, 0],
#         [0, -1, -1, -1,  0, 0],
#         [0,  0,  0,  0,  0, 0],
#         [0,  0,  0,  0,  0, 0],
#         [0,  0,  0,  0,  0, 0],
#         [0,  0,  0,  0,  0, 0]
#         ])
#     assert collect_sequences(g, -1) == 3

# def test_row_white2():
#     g = np.array([
#         [0,  0,  0,  0,  0, 0],
#         [0,  1,  1,  1,  0, 0],
#         [0, -1, -1, -1, -1, 0],
#         [0,  0,  0,  0,  0, 0],
#         [0,  0,  0,  0,  0, 0],
#         [0,  0,  0,  0,  0, 0]
#         ])
#     assert collect_sequences(g, -1) == 4

# def test_row_white3():
#     g = np.array([
#         [0,  0,  0,  0,  0, 0],
#         [0,  1,  1,  1,  0, 0],
#         [0,  0,  0,  0,  0, 0],
#         [0,  0,  0, -1,  0, 0],
#         [0,  0,  0, -1,  0, 0],
#         [0,  0,  0,  0,  0, 0]
#         ])
#     assert collect_sequences(g, -1) == 2

# def test_row_white4():
#     g = np.array([
#         [0,  0,  0,  0,  0,-1],
#         [0,  1,  1,  0,  0, 0],
#         [0,  0,  1, -1,  0, 0],
#         [0,  0, -1,  1,  0, 0],
#         [0, -1,  0,  0,  1, 0],
#         [0,  0,  0,  0,  0, 0]
#         ])
#     assert collect_sequences(g, -1) == 3

# def test_row_white5():
#     g = np.array([
#         [0,  0,  0,  0,  0,-1],
#         [0, -1,  1,  0,  0, 0],
#         [0,  0, -1,  1,  0, 0],
#         [0,  0,  1, -1,  0, 0],
#         [0,  1,  0,  0,  -1, 0],
#         [0,  0,  0,  0,  0, 0]
#         ])
#     assert collect_sequences(g, -1) == 4

# def test_row2():
#     g = np.array([
#         [0,  0,  0,  0,  0, 0],
#         [0,  0,  1,  1,  1, 0],
#         [1,  0,  0,  0,  0, 0],
#         [0,  0,  0,  0,  1, 0],
#         [1,  1,  0,  1,  1, 0],
#         [1,  1,  0,  1,  1, 0]
#         ])
#     row = Row(3, Position(1,2), 1, g)
#     assert row.is_a_grouped_free_three()

# def test_row3():
#     g = np.array([
#         [0,  0,  0,  0,  0,  0],
#         [0,  1,  1,  1,  0, -1],
#         [1,  0,  0,  0,  0,  0],
#         [0,  0,  0,  0,  1,  0],
#         [1,  1,  0,  1,  1,  0],
#         [1,  1,  0,  1,  1,  0]
#         ])
#     row = Row(3, Position(1,1), 1, g)
#     assert not row.is_a_grouped_free_three()

# def test_row4():
#     g = np.array([
#         [ 0,  0,  0,  0,  0,  0],
#         [-1,  0,  1,  1,  1,  0],
#         [ 1,  0,  0,  0,  0,  0],
#         [ 0,  0,  0,  0,  1,  0],
#         [ 1,  1,  0,  1,  1,  0],
#         [ 1,  1,  0,  1,  1,  0]
#         ])
#     row = Row(3, Position(1,1), 1, g)
#     assert not row.is_a_grouped_free_three()

# def test_row5():
#     g = np.array([
#         [ 0,  0,  0,  0,  0,  0],
#         [ 0, -1,  1,  1,  1,  0],
#         [ 1,  0,  0,  0,  0,  0],
#         [ 0,  0,  0,  0,  1,  0],
#         [ 1,  1,  0,  1,  1,  0],
#         [ 1,  1,  0,  1,  1,  0]
#         ])
#     row = Row(3, Position(1,1), 1, g)
#     assert not row.is_a_grouped_free_three()


# def test_col1():
#     g = np.array([
#         [0,  0,  0,  0,  0, 0],
#         [0,  1,  1,  1,  0, 0],
#         [1,  0,  1,  0,  0, 0],
#         [0,  0,  1,  0,  1, 0],
#         [1,  1,  0,  1,  1, 0],
#         [1,  1,  0,  1,  1, 0]
#         ])
#     col = Column(3, Position(1,2), 1, g)
#     assert col.is_a_grouped_free_three()

# def test_col2():
#     g = np.array([
#         [0,  0,  0,  0,  0, 0],
#         [0,  1,  0,  1,  0, 0],
#         [1,  0,  1,  0,  0, 0],
#         [0,  0,  1,  0,  1, 0],
#         [1,  1,  1,  1,  1, 0],
#         [1,  1,  0,  1,  1, 0]
#         ])
#     col = Column(3, Position(2,2), 1, g)
#     assert col.is_a_grouped_free_three()

# def test_col3():
#     g = np.array([
#         [0,  0, -1,  0,  0, 0],
#         [0,  1,  0,  1,  0, 0],
#         [1,  0,  1,  0,  0, 0],
#         [0,  0,  1,  0,  1, 0],
#         [1,  1,  1,  1,  1, 0],
#         [1,  1,  0,  1,  1, 0]
#         ])
#     col = Column(3, Position(2,2), 1, g)
#     assert not col.is_a_grouped_free_three()


# def test_col4():
#     g = np.array([
#         [0,  0,  0,  0,  0, 0],
#         [0,  1,  1,  1,  0, 0],
#         [1,  0,  1,  0,  0, 0],
#         [0,  0,  1,  0,  1, 0],
#         [1,  1,  0,  1,  1, 0],
#         [1,  1, -1,  1,  1, 0]
#         ])
#     col = Column(3, Position(1,2), 1, g)
#     assert not col.is_a_grouped_free_three()


# def test_col5():
#     g = np.array([
#         [0,  0,  0,  0,  0, 0],
#         [0,  1, -1,  1,  0, 0],
#         [1,  0,  1,  0,  0, 0],
#         [0,  0,  1,  0,  1, 0],
#         [1,  1,  1,  1,  1, 0],
#         [1,  1,  0,  1,  1, 0]
#         ])
#     col = Column(3, Position(2,2), 1, g)
#     assert not col.is_a_grouped_free_three()

# def test_diag1():
#     g = np.array([
#         [0,  0,  0,  0,  0, 0],
#         [0,  1,  1,  1,  0, 0],
#         [1,  0,  1,  0,  0, 0],
#         [0,  0,  1,  1,  1, 0],
#         [1,  1,  0,  1,  0, 0],
#         [1,  1,  0,  1,  1, 0]
#         ])
#     diag = Diagonal(3, Position(1,1), 1, g, True)
#     assert diag.is_a_grouped_free_three()

# def test_diag2():
#     g = np.array([
#         [0,  0,  0,  0,  0, 0],
#         [0,  0,  1,  1,  0, 0],
#         [1,  0,  1,  0,  0, 0],
#         [0,  0,  1,  1,  1, 0],
#         [1,  1,  0,  1,  1, 0],
#         [1,  1,  0,  1,  1, 0]
#         ])
#     diag = Diagonal(3, Position(2,2), 1, g, True)
#     assert diag.is_a_grouped_free_three()

# def test_diag3():
#     g = np.array([
#         [0,  0,  0,  0,  0, 0],
#         [0,  1,  1,  1,  0, 0],
#         [1,  0,  1,  0,  0, 0],
#         [0,  0,  1,  1,  1, 0],
#         [1,  1,  0,  1,  0, 0],
#         [1,  1,  0,  1,  1, -1]
#         ])
#     diag = Diagonal(3, Position(1,1), 1, g, True)
#     assert not diag.is_a_grouped_free_three()


# def test_diag4():
#     g = np.array([
#         [-1, 0,  0,  0,  0, 0],
#         [0,  0,  1,  1,  0, 0],
#         [1,  0,  1,  0,  0, 0],
#         [0,  0,  1,  1,  1, 0],
#         [1,  1,  0,  1,  1, 0],
#         [1,  1,  0,  1,  1, 0]
#         ])
#     diag = Diagonal(3, Position(2,2), 1, g, True)
#     assert not diag.is_a_grouped_free_three()

# def test_diag5():
#     g = np.array([
#         [0,  0,  0,  0,  0, 0],
#         [0, -1,  1,  1,  0, 0],
#         [1,  0,  1,  0,  0, 0],
#         [0,  0,  1,  1,  1, 0],
#         [1,  1,  0,  1,  1, 0],
#         [1,  1,  0,  1,  1, 0]
#         ])
#     diag = Diagonal(3, Position(2,2), 1, g, True)
#     assert not diag.is_a_grouped_free_three()

# def test_rdiag1():
#     g = np.array([
#         [0,  0,  0,  0,  0, 0],
#         [0,  1,  1,  1,  0, 0],
#         [1,  0,  1,  1,  0, 0],
#         [0,  0,  1,  1,  1, 0],
#         [1,  1,  0,  1,  0, 0],
#         [0,  1,  0,  1,  1, 0]
#         ])
#     diag = Diagonal(3, Position(2,3), 1, g, False)
#     assert diag.is_a_grouped_free_three()

# def test_rdiag2():
#     g = np.array([
#         [0,  0,  0,  0,  0, 0],
#         [0,  1,  1,  1,  1, 0],
#         [1,  0,  1,  1,  0, 0],
#         [0,  0,  1,  1,  1, 0],
#         [1,  0,  0,  1,  0, 0],
#         [0,  1,  0,  1,  1, 0]
#         ])
#     diag = Diagonal(3, Position(1,4), 1, g, False)
#     assert diag.is_a_grouped_free_three()

# def test_rdiag3():
#     g = np.array([
#         [0,  0,  0,  0,  0, -1],
#         [0,  1,  1,  1,  0,  0],
#         [1,  0,  1,  1,  0,  0],
#         [0,  0,  1,  1,  1,  0],
#         [1,  1,  0,  1,  0,  0],
#         [0,  1,  0,  1,  1,  0]
#         ])
#     diag = Diagonal(3, Position(2,3), 1, g, False)
#     assert not diag.is_a_grouped_free_three()


# def test_rdiag4():
#     g = np.array([
#         [0,  0,  0,  0,  0, 0],
#         [0,  1,  1,  1,  1, 0],
#         [1,  0,  1,  1,  0, 0],
#         [0,  0,  1,  1,  1, 0],
#         [1,  0,  0,  1,  0, 0],
#         [-1, 1,  0,  1,  1, 0]
#         ])
#     diag = Diagonal(3, Position(1,4), 1, g, False)
#     assert not diag.is_a_grouped_free_three()


# def test_rdiag5():
#     g = np.array([
#         [0,  0,  0,  0,  0, 0],
#         [0,  1,  1,  1,  1, 0],
#         [1,  0,  1,  1,  0, 0],
#         [0,  0,  1,  1,  1, 0],
#         [1, -1,  0,  1,  0, 0],
#         [0,  1,  0,  1,  1, 0]
#         ])
#     diag = Diagonal(3, Position(1,4), 1, g, False)
#     assert not diag.is_a_grouped_free_three()