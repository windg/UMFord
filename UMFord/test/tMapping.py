import unittest
from mapping import BOF
import scipy.io as sio
import matplotlib.pyplot as plt
import numpy as np
import glob 
from main import removePoints
class TestBOF(unittest.TestCase):
    def test_verifyOrin(self):
        self.assertEqual(self.BOF.l0.shape[0],1)
    
    def test_verifyExpand(self):
        r = 30
        robot_pos = np.array([0,0])
        self.BOF.expandMap(np.array(robot_pos),r)
        self.assertEqual(self.BOF.l.shape,(r*2,r*2))
        self.assertTrue(( self.BOF.orig == np.array([-r,-r])).all())
        
    def test_verifyOneScan(self):
        SCANFilesDir = 'C:\\ProjectData\\FordSample\\IJRR-Dataset-1-subset\\SCANS\\Scan'
        PoseFile = 'L:\\Projects\\SensorFusion\\Source\\Pose.mat'
        files = glob.glob(SCANFilesDir +'*.mat')
        print(files[0])
        SCAN = sio.loadmat(files[1])
        Pose = sio.loadmat(PoseFile)
        Pose = Pose['Pose'][0][0]
        SCAN = SCAN['SCAN']
        pos_utime = Pose['utime']
        ind = np.argmin(np.abs(SCAN['timestamp_laser']-pos_utime))
        
        pos =  np.append(Pose['pos'][ind][0:2], Pose['rph'][ind][2])
#        pos = np.array([1,1,0])
        print(type(pos))
        vel = Pose['vel'][ind]
        orien = Pose['rph'][ind]
        print(orien.shape)
        
        pts = np.array(SCAN['XYZ'])
        pts = pts[0][0]
        pts = np.transpose((pts))
        print(pts.shape)
        self.BOF = BOF(pos[0:2], np.array([[0]]),cellsize=1)
        r = 5
        pts = removePoints(pts,r,[-2,2])
        self.BOF.expandMap(pos,r)
#        pts_sample = pts[np.random.choice(pts.shape[0],1000),:] 
#        pts_sample = pts 
        pts_sample = np.array([[-4.9,-4.9,1]])
        print('sample size' ,pts_sample.shape)
#        fig = plt.figure(figsize=[15,15])
#        ax1 = fig.add_subplot(211,  aspect='equal')
#        ax1.scatter(pts_sample[:,0],pts_sample[:,1],s=0.1,c=pts_sample[:,2])
        for i in range(pts_sample.shape[0]):
            self.BOF.updateGrid(pos,pts_sample[i,:])
#        print(self.BOF.l)
        self.BOF.viewMap()
    def setUp(self):
        self.BOF = BOF(np.array([0,0]), np.array([[0]]))

if __name__=='__main__':
    unittest.main()
    