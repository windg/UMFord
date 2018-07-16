import scipy.io as sio
import numpy as np
import glob 
import matplotlib.pyplot as plt
from mapping import BOF
def readPoint(file):
    # Read the point cloud data from .mat files 
    # z is the vertical direction
    SCAN = sio.loadmat(file)
    SCAN = SCAN['SCAN']
    pt = np.array(SCAN['XYZ'])
    pt = pt[0][0]
    pt = np.transpose((pt))
    return pt

def removePoints(pt, r,zlmt,slfr=5):
    # Remove points oudside of limit
    # limits = array([[xmin,xmax],[ymin,ymax]])
    # zoffest is a scalar and every points below zoffset is included
    inside = []
    for n in range(len(pt)):
        if pt[n,0]**2+pt[n,1]**2< r**2 and \
        zlmt[0]<pt[n,2]<zlmt[1] and \
        pt[n,0]**2+pt[n,1]**2 > slfr**2:
            inside.append(n)
    return pt[inside] 
def findPose(pt_utime, pose_utime):
    # pt_utime is a scalar for the time of the point cloud
    # pose_utime is the nparray for all the utime
    ind = np.argmin(np.abs(pt_utime - pose_utime))
    return ind

def generator(folder):
    files = glob.glob(folder +'*.mat')
    for file in files:
        print('File name is {0}'.format(file))
        SCAN = sio.loadmat(file)
        SCAN = SCAN['SCAN']
        pt = np.array(SCAN['XYZ'])
        pt = pt[0][0]
        pt = np.transpose((pt))
        yield pt, SCAN

if __name__ == '__main__':
    # Path
    SCANFilesDir = 'C:\\ProjectData\\FordSample\\IJRR-Dataset-1-subset\\SCANS\\Scan'
    ImageDir = 'C:\\ProjectData\FordSample\\IJRR-Dataset-1-subset\\IMAGES\\'
#    PoseFile = 'L:\\Projects\\SensorFusion\\Source\\Pose.mat'
    PoseFile = 'IMU.mat'
    # Variables
    r = 15
    zlmt = np.array([-2,4])
    nsample = 10000
    Pose = sio.loadmat(PoseFile)
    Pose = Pose['IMU'][0][0]
    pos_utime = Pose['utime']
    pos =  np.append(Pose['pos'][0][0:2], Pose['rph'][0][2])
   
    file = generator(SCANFilesDir)
    count = 1
    fig  = plt.figure(figsize=[15,15]) 
    ax1= fig.add_subplot(211,  aspect='equal')
    ax2 = fig.add_subplot(212, aspect='equal')
    for[pt, SCAN] in file:
       
        r = 15
        ind = np.argmin(np.abs(SCAN['timestamp_laser']-pos_utime))
        pos =  np.append(Pose['pos'][ind][0:2], Pose['rph'][ind][2])
        print(pos)
        if count == 1:
            bof = BOF(pos[0:2], np.array([[0]]),cellsize=1)
            count += 1
        pt = removePoints(pt,r,zlmt)
#        ax1.clear()
#        ax1.scatter(pt[:,0],pt[:,1],s=0.1,c=pt[:,2])
#        plt.pause(0.01)
        pts_sample = pt[np.random.choice(pt.shape[0],nsample),:] 
        for i in range(pts_sample.shape[0]):
            bof.updateGrid(pos,pts_sample[i,:],r)
        ax2.clear()
        ax2.scatter(pts_sample[:,0],pts_sample[:,1],s=3,c=pts_sample[:,2])
        bof.viewMap(ax=ax1)
        
    
#    pt = next(file)
#    
#    pt = removePoints(pt,r=r,zlmt=zlmt)
#    ax2.scatter(pt[:,0],pt[:,1],s=0.1,c=pt[:,2])
#    
#    Grid = BOF(np.array([0,0]), np.array([1]))
#    