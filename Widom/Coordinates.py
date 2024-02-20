import numpy as np

class Coordinates:

    @staticmethod
    def triclinic_transformation(d: list):
        # d equals [lx,ly,lz,alpha,beta,gamma]
        d[3], d[4], d[5] = np.pi*d[3]/180, np.pi*d[4]/180, np.pi*d[5]/180
        M = np.array([[d[0], d[1]*np.cos(d[5]), d[2]*np.cos(d[4])],
                      [0, d[1]*np.sin(d[5]), -d[2]*np.sin(d[4])*np.cos(d[3])],
                      [0, 0, d[2]*np.sin(d[4])*np.sin(d[3])]])
        
        return M
    