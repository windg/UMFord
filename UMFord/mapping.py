# -*- coding: utf-8 -*-
import numpy as np
from math import sqrt, atan2, log, exp
import matplotlib.pyplot as plt
class BOF:
    def __init__(self,orig, initmap, cellsize=1, sensorconeangle = 0.1):
        self.orig = orig
        self.l0 = initmap
        self.l = initmap
        self._lfree = log(0.3/0.7)
        self._locc = log(0.6/0.4)
        self._cellsize = cellsize
        self._sensorconeangle = sensorconeangle
        self.ax = 'none'
        
    def expandMap(self,robot_pos,r):
        orig_map_shape = self.l.shape
        n_lft = np.zeros(2,dtype='int32')
        n_rght = np.zeros(2,dtype='int32')
        new_shape = np.zeros(2,dtype='int32')
        new_orig = np.zeros(2)
        for i in range(2):
            d = robot_pos[i]-self.orig[i]
            extra = r-d
            n_lft[i] = np.ceil((extra)/self._cellsize) *(extra>0)  
            extra = r+d - orig_map_shape[i]*self._cellsize
            n_rght[i] = np.ceil((extra)/self._cellsize) *(extra>0)  
            new_shape[i] = n_lft[i] + n_rght[i] + orig_map_shape[i]
            new_orig[i] =  self.orig[i]- n_lft[i]*self._cellsize
               
        new_map = np.zeros(new_shape)
        new_map[n_lft[0]:n_lft[0]+orig_map_shape[0],n_lft[1]:n_lft[1]+orig_map_shape[1]]=\
            self.l
        self.l = new_map
        self.orig = new_orig
        return [n_lft[0],n_lft[0]+orig_map_shape[0]], [n_lft[1],n_lft[1]+orig_map_shape[1]]
        
    def setSensor(self,lfree, locc):
        self._lfree = lfree
        self._locc = locc
    
    def updateGrid(self,xt,zt,r):
        # xt: robot location [x,y,theta]
        # zt: object location related to robot [x,y]
        [loc_x, loc_y] = self.expandMap(xt,r)
        for i in range(loc_x[0],loc_x[1]):
            for j in range(loc_y[0],loc_y[1]):
                old = self.l[i][j]
                
                self.l[i][j] += self.inverseMdl(np.array([i,j]),xt,zt) 
#                if old!= 0 and self.inverseMdl(np.array([i,j]),xt,zt)!=0:
#                    print('old value = ',old)
#                    print('new value = ',self.l[i][j])
    def getGlobalCoord(self,m):
        return self.orig + (m)*self._cellsize +0.5*self._cellsize
        
    
    def viewMap(self, ax='none'):
        self.ax=ax
        if self.ax == 'none':
            fig, self.ax = plt.subplots()
        else:
            ax.clear()
        p_map = 1-1/(1+np.exp(self.l))
       
        self.ax.imshow(np.rot90(1.0-p_map), cmap='gray')
        
        plt.pause(0.01)
        
    def inverseMdl(self, m, xt,zt):
        # m: cell [labelx, labely]
        # xt: robot location [x,y,theta]
        # zt: object location related to robot [x,y]
        p = self.getGlobalCoord(m)
        r = sqrt((xt[0]-p[0])**2+(xt[1]-p[1])**2)
        psi = atan2(p[1]-xt[1],p[0]-xt[0]) - xt[2]
        rz = sqrt(zt[0]**2+zt[1]**2)
        thetaz = atan2(zt[1],zt[0]) - xt[2]
        alpha = self._cellsize/sqrt(2)
        beta = self._sensorconeangle
        if r> rz+alpha or abs(psi-thetaz) > beta/2:
            return self.l[m[0]][m[1]]
        if abs(r -rz)<alpha :
            return self._locc
        if r<= rz:
            return self._lfree
        