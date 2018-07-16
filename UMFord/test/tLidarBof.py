import unittest
from LidarBof import LidarBof
from numpy import testing as nt
import numpy as np
from parameterized import parameterized

class TestLidarBof(unittest.TestCase):

    def test_verifyFindEmptyCell(self):
        robotPos = np.array([0,0])
        objPos = np.array([0,4])
        expected = np.array([[0,0],[0,1],[0,2],[0,3]])
        actual = self.obj.findEmptyCell(robotPos,objPos)
        # print(actual)
        diag = 'Center should be numpy array [0,0]'
        nt.assert_array_equal(actual, expected, diag)

        robotPos = np.array([0, 0])
        objPos = np.array([4,0])
        expected = np.array([[0, 0], [1, 0], [2, 0], [3, 0]])
        actual = self.obj.findEmptyCell(robotPos, objPos)
        # print(actual)
        nt.assert_array_equal(actual, expected, diag)


        robotPos = np.array([0, 0])
        objPos = np.array([3,4])
        expected = np.array([[0, 0], [0, 1], [1, 1],[1,2],[2,2],[2,3]])
        actual = self.obj.findEmptyCell(robotPos, objPos)
        nt.assert_array_equal(actual, expected, diag)
    def setUp(self):
        origin = np.array([0, 0])
        initGrid = np.array([[0]])
        self.obj = LidarBof(origin, initGrid)

if __name__=='__main__':
    unittest.main()
