# -*- coding: utf-8 -*-

import numpy as np
from math import sqrt, atan2, log, exp, cos, sin
import matplotlib.pyplot as plt
from Grid import grid
class LidarBof:
    def __init__(self,origin, initGrid,r=15, zlmt=[-2,2], cellsize=1):
        self.origin = origin
        self.l0 = grid(res=cellsize)
        self.l = grid(res=cellsize)
        self._lfree = log(0.3/0.7)
        self._locc = log(0.6/0.4)
        self._cellsize = cellsize
        self.ax = 'none'
        self._r = r
        self._zlmt = zlmt
        
    def ptToGrid(self, robot_pos, pt):
#        Convert point cloud to a local grid
#        robot_pos: current robot position [x, y, theta]
#        pt: 2D numpy array for point cloud [[x1, y1, z1], [x2, y2, z2]...]
        ngrid = np.ceil((self._r-0.5*self._cellsize)/self._cellsize)
        localGrid = grid()
        pt = pt[:,0:2]
        Rot = np.array([[cos(robot_pos[2]), -sin(robot_pos[2])],[ sin(robot_pos[2]), cos(robot_pos[2])]])
        pt = np.transpose(np.matmul(Rot,pt.transpose()))
        for i in range(pt.shape[0]):
            empcell = self.findEmptyCell(robot_pos, pt[i,:])


        return False
        
    def updateGrid(self,robot_pos,pts):
#        Update grid using simple BOF
#        l_t = l_tminus + localGrid - l0
        # Expand grid according to the current robot position
        self.l.expandGrid(robot_pos,self._r)
        # Remove points outside of radius
        robot_cell = self.l.findCell(robot_pos)
        pts = self.removePoints(pts,self._r,self._zlmt)
        pts = pts[:,0:2]
        Rot = np.array([[cos(robot_pos[2]), -sin(robot_pos[2])],[ sin(robot_pos[2]), cos(robot_pos[2])]])
        pts = np.transpose(np.matmul(Rot,pts.transpose()))
        # Update the grid
        for i in range(pts.shape[0]):
            obj_cell = self.l.findCell(pts[i, :])
            empcell = self.findEmptyCell(robot_cell, obj_cell)



        return False

    def findEmptyCell(self,robot_pos,pt):
        start = self.l.findCell(robot_pos)
        end = self.l.findCell((pt))
        if start[0]<end[0]:
            xgrid = [i for i in range(int(np.floor(start[0])), int(np.ceil(end[0])))]
        elif start[0]>end[0]:
            xgrid = [i for i in range(int(np.floor(end[0])),int(np.ceil(start[0])))]
        else:
            xgrid = [np.floor(end[0])]

        if start[1]<end[1]:
            ygrid = [i for i in range(int(np.floor(start[1])),int(np.ceil(end[1])))]
        elif start[1]>end[1]:
            ygrid = [i for i in range(int(np.floor(start[1])),int(np.ceil(end[1])))]
        else:
            ygrid = [np.floor(start[1])]
        if np.floor(start[0]) == np.floor(end[0]):
            return np.transpose(np.array([[x for x in np.ones(len(ygrid))*np.floor(start[0])], ygrid],dtype=int))

        if np.floor(start[1]) == np.floor(end[1]):
            return np.transpose(np.array([xgrid,[y for y in np.ones(len(xgrid))*np.floor(start[1])]],dtype=int))

        p = end - start
        slope = p[1]/p[0]

        yvalue = np.floor(slope * (xgrid - start[0]) + start[1])
        xvalue = np.floor((ygrid-start[1])/slope + start[0])

        result1 = np.transpose(np.array([xgrid,yvalue],dtype=int))
        result2 = np.transpose(np.array([xvalue,ygrid],dtype=int))
        return np.unique(np.concatenate((result1,result2),axis=0),axis=0)
        
    def veiwGrid(self):
        return False
    
    def viewLocalGrid(self):
        return False

    def removePoints(self, pt, r, zlmt, slfr=5):
        # Remove points oudside of limit
        # limits = array([[xmin,xmax],[ymin,ymax]])
        # zoffest is a scalar and every points below zoffset is included
        # slfr is the radius of self
        inside = []
        for n in range(len(pt)):
            if pt[n, 0] ** 2 + pt[n, 1] ** 2 < r ** 2 and \
                    zlmt[0] < pt[n, 2] < zlmt[1] and \
                    pt[n, 0] ** 2 + pt[n, 1] ** 2 > slfr ** 2:
                inside.append(n)
        return pt[inside]

#     def expandGrid(self,robot_pos,r):
# #        Expand global grid according the robot posision and the sensor radius
#         orig_map_shape = self.l.shape
#         n_lft = np.zeros(2,dtype='int32')
#         n_rght = np.zeros(2,dtype='int32')
#         new_shape = np.zeros(2,dtype='int32')
#         new_orig = np.zeros(2)
#         for i in range(2):
#             d = robot_pos[i]-self.origin[i]
#             extra = r-d
#             n_lft[i] = np.ceil((extra)/self._cellsize) *(extra>0)
#             extra = r+d - orig_map_shape[i]*self._cellsize
#             n_rght[i] = np.ceil((extra)/self._cellsize) *(extra>0)
#             new_shape[i] = n_lft[i] + n_rght[i] + orig_map_shape[i]
#             new_orig[i] =  self.origin[i]- n_lft[i]*self._cellsize
#
#         new_map = np.zeros(new_shape)
#         new_map[n_lft[0]:n_lft[0]+orig_map_shape[0],n_lft[1]:n_lft[1]+orig_map_shape[1]]=\
#             self.l
#         self.l = new_map
#         self.origin = new_orig
#         return [n_lft[0],n_lft[0]+orig_map_shape[0]], [n_lft[1],n_lft[1]+orig_map_shape[1]]
if __name__=='__main__':
    origin = np.array([0, 0])
    initGrid = np.array([[0]])
    obj = LidarBof(origin, initGrid)