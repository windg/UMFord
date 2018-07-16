import scipy.io as sio
import numpy as np
#import mayavi.mlab
import matplotlib.pyplot as plt
#from mpl_toolkits.mplot3d import Axes3D
import glob 

DataFile = 'L:\\Projects\\SensorFusion\\Source\\DATA.mat'
#DATA = sio.loadmat(DataFile)
SCANFilesDir = 'C:\ProjectData\\FordSample\\IJRR-Dataset-1-subset\\SCANS\\Scan'
ImageDir = 'C:\\ProjectData\FordSample\\IJRR-Dataset-1-subset\\IMAGES\\'
PoseFile = 'L:\\Projects\\SensorFusion\\Source\\Pose.mat'
files = glob.glob(SCANFilesDir +'*.mat')
plt.ion()
fig = plt.figure(figsize=[15,15])
ax = fig.add_subplot(111,  aspect='equal')
x = []
y = []
sc = ax.scatter(x, y, s=0.001)
plt.draw
for SCANFileNum in files:
#SCANFileNum = '1000'
    print(SCANFileNum)
    SCAN = sio.loadmat(SCANFileNum)
    SCAN = SCAN['SCAN']
    pt = np.array(SCAN['XYZ'])
    pt = pt[0][0]
    pt = np.transpose((pt))
    ax.clear()
    ax.scatter(pt[:, 0], pt[:, 1], s=0.001, cmap='gray')
#    x = pt[:, 0]
#    y = pt[:, 1]
#    sc.set_offsets(np.c_[x,y])
#    fig.canvas.draw_idle()
    # velo[:, 3], # reflectance values
#mayavi.mlab.show()
    
    plt.pause(0.1)
#plt.show()
#fig =  mayavi.mlab.figure(bgcolor=(0, 0, 0), size=(1280*2, 720*2))

#mayavi.mlab.points3d(
#        pt[:, 0],   # x
#        pt[:, 1],   # y
#        pt[:, 2],   # z
#        pt[:, 2],   # Height data used for shading
#        mode="point", # How to render each point {'point', 'sphere' , 'cube' }
#        colormap='spectral',  # 'bone', 'copper',
#        #color=(0, 1, 0),     # Used a fixed (r,g,b) color instead of colormap
#        scale_factor=100,     # scale of the points
#        line_width=10,        # Scale of the line, if any
#        figure=fig,
#    )
#    # velo[:, 3], # reflectance values


