import unittest
from numpy import testing as nt
import numpy as np
from Grid import grid
class TestGrid(unittest.TestCase):
    def test_verifyInit(self):
        g = grid(res=0.5)
        expected = np.array([[0]])
        actual = g.grid
        diag = 'Init grid should be numpy 2d array with dimension [1,1] and value 0'
        nt.assert_array_equal(actual,expected,diag)
        expected = np.array([0,0])
        actual = g.center
        diag = 'Center should be numpy array [0,0]'
        nt.assert_array_equal(actual, expected, diag)

        expected = np.array([-0.5*0.5,-0.5*0.5])
        actual = g.leftbottom
        diag = 'Center should be numpy array [0,0]'
        nt.assert_array_equal(actual, expected, diag)

    def test_verifyFindCell(self):
        g = grid(res=2)
        pos = np.array([3,7])
        expected = np.array([2,4])
        actual = g.findCell(pos)
        diag = ''
        nt.assert_array_equal(actual, expected, diag)

        pos = np.array([-1.5,-2.5])
        expected = np.array([-1, -1])
        actual = g.findCell(pos)
        diag = ''
        nt.assert_array_equal(actual, expected, diag)
    # def test_veridyExpandGrid(self):
    #     g = grid()
    #     g.expandGrid(3,4)
    #     expected = np.array((4,5))
    #     actual = np.array(g.grid.shape)
    #     diag = ''
    #     nt.assert_array_equal(actual, expected, diag)
    def test_verifySetCenter(selfself):
        g = grid()
        robot_pos = np.array([0,0])
        r = 15
        g.expandGrid(robot_pos,r)
        print(g.leftbottom)
        g.setCenter(np.array([1,1]))
        print(g.leftbottom)


if __name__=='__main__':
    unittest.main()