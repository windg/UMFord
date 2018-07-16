import numpy as np
class grid:
    def __init__(self, res=1):
        self.grid = np.array([[0]])
        self.center = np.array([0,0])
        self._res = res
        self.leftbottom = np.array([-0.5*res,-0.5*res])

    def findCell(self, pos):
        pos_local = pos - self.leftbottom
        result = np.floor(pos_local/self._res)
        return result.astype(np.int64)
    # def expandGrid(self,nrow,ncolumn):
    #     return np.zeros([self.grid.shape[0]+nrow, self.grid.shape[1]+ncolumn])

    def expandGrid(self,robot_pos,r):
#        Expand global grid according the robot posision and the sensor radius
        orig_map_shape = self.grid.shape
        n_lft = np.zeros(2,dtype='int32')
        n_rght = np.zeros(2,dtype='int32')
        new_shape = np.zeros(2,dtype='int32')
        new_orig = np.zeros(2)
        for i in range(2):
            d = robot_pos[i]-self.leftbottom[i]
            extra = r-d
            n_lft[i] = np.ceil((extra)/self._res) *(extra>0)
            extra = r+d - orig_map_shape[i]*self._res
            n_rght[i] = np.ceil((extra)/self._res) *(extra>0)
            new_shape[i] = n_lft[i] + n_rght[i] + orig_map_shape[i]
            new_orig[i] =  self.leftbottom[i]- n_lft[i]*self._res

        new_map = np.zeros(new_shape)
        new_map[n_lft[0]:n_lft[0]+orig_map_shape[0],n_lft[1]:n_lft[1]+orig_map_shape[1]]=\
            self.grid
        self.grid = new_map
        self.leftbottom = new_orig
        return [n_lft[0], n_lft[0]+orig_map_shape[0]], [n_lft[1], n_lft[1]+orig_map_shape[1]]

    def setCenter(self,center):
        self.center = center
        ngrid = np.array(self.grid.shape)
        self.leftbottom = center - ngrid*self._res/2
    def findEmptyCell(self, robot_pos, pt):
        start = self.findCell(robot_pos)
        end = self.findCell((pt))
        if start[0] < end[0]:
            xgrid = [i for i in range(int(np.floor(start[0])), int(np.ceil(end[0])))]
        elif start[0] > end[0]:
            xgrid = [i for i in range(int(np.floor(end[0])), int(np.ceil(start[0])))]
        else:
            xgrid = [np.floor(end[0])]

        if start[1] < end[1]:
            ygrid = [i for i in range(int(np.floor(start[1])), int(np.ceil(end[1])))]
        elif start[1] > end[1]:
            ygrid = [i for i in range(int(np.floor(start[1])), int(np.ceil(end[1])))]
        else:
            ygrid = [np.floor(start[1])]
        if np.floor(start[0]) == np.floor(end[0]):
            return np.transpose(np.array([[x for x in np.ones(len(ygrid)) * np.floor(start[0])], ygrid], dtype=int))

        if np.floor(start[1]) == np.floor(end[1]):
            return np.transpose(np.array([xgrid, [y for y in np.ones(len(xgrid)) * np.floor(start[1])]], dtype=int))

        p = end - start
        slope = p[1] / p[0]

        yvalue = np.floor(slope * (xgrid - start[0]) + start[1])
        xvalue = np.floor((ygrid - start[1]) / slope + start[0])

        result1 = np.transpose(np.array([xgrid, yvalue], dtype=int))
        result2 = np.transpose(np.array([xvalue, ygrid], dtype=int))
        return np.unique(np.concatenate((result1, result2), axis=0), axis=0)


