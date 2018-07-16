import scipy.io as sio
import numpy as np
import matplotlib.pyplot as plt
import glob 
class pcl:
    
    def __init__(self,pt,xlimt,ylimt, zoffset):
         self.pt = pt
         xlimt = np.array([xlimt])
         ylimt = np.array([ylimt])
         self.range = np.concatenate((xlimt,ylimt),axis=0)
         self.ylimt = ylimt
         self.zoffset = zoffset
         
    def genOG(self, res):
        numGrid = self.range.ptp(axis=1)*res
        self.og = np.zeros(numGrid)
         
        for pt in self.pt:
            sub = np.uint32(np.floor((pt[0:2] - self.range[:,0])*res)) 
            self.og[sub.tolist()[0],sub.tolist()[1]] = 256
#        print(self.og.shape)
         
    def rmOutside(self):
        inside = []
        for n in range(len(self.pt)):
            if self.range[0,0]<self.pt[n,0]<self.range[0,1] and \
            self.range[1,0]<self.pt[n,1]<self.range[1,1] and \
            self.zoffset<self.pt[n, 2]:
                inside.append(n)
        self.pt = self.pt[inside] 
                

DataFile = 'L:\\Projects\\SensorFusion\\Source\\DATA.mat'
#DATA = sio.loadmat(DataFile)
SCANFilesDir = 'C:\\ProjectData\\FordSample\\IJRR-Dataset-1-subset\\SCANS\\Scan'
ImageDir = 'C:\\ProjectData\FordSample\\IJRR-Dataset-1-subset\\IMAGES\\'
PoseFile = 'L:\\Projects\\SensorFusion\\Source\\Pose.mat'
plt.ion()
files = glob.glob(SCANFilesDir +'*.mat')
fig = plt.figure(figsize=[15,15])
ax = fig.add_subplot(211,  aspect='equal')
ax2 = fig.add_subplot(212,  aspect='equal')


for SCANFileNum in files:
    print(SCANFileNum)
    SCAN = sio.loadmat(SCANFileNum)
    SCAN = SCAN['SCAN']
    pt = np.array(SCAN['XYZ'])
    pt = pt[0][0]
    pt = np.transpose((pt))
    pt1 = pcl(pt,[-15, 15],[-15,15],-2)
    pt1.rmOutside()
    pt1.genOG(3)
    ax.clear()
    ax2.clear()
    ax.scatter(pt1.pt[:,0],pt1.pt[:,1],s=0.1)
    ogplot = ax2.imshow(np.rot90(pt1.og))
    ogplot.set_cmap('gray')
    plt.pause(0.01)
#SCANFileNum = '1000'
#SCAN = sio.loadmat(SCANFilesDir + SCANFileNum + '.mat')
#SCAN = SCAN['SCAN']
#pt = np.array(SCAN['XYZ'])
#pt = pt[0][0]
#pt = np.transpose((pt))
#
#pt1 = pcl(pt,[-40, 40],[-40,40],-2)
#pt1.rmOutside()
#fig = plt.figure(figsize=[15,15])
#ax = fig.add_subplot(211,  aspect='equal')
#ax.scatter(pt1.pt[:,0],pt1.pt[:,1],s=0.1)
##
#pt1.genOG(10)
#
#ax2 = fig.add_subplot(212,  aspect='equal')
#ogplot = ax2.imshow(np.rot90(pt1.og))
#ogplot.set_cmap('gray')