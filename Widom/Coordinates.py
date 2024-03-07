import numpy as np

class Coordinates:

    @staticmethod
    def triclinic_transformation(d: list):
        # d equals [lx,ly,lz,alpha,beta,gamma]

        M = np.array([[d[0], d[1]*np.cos(np.radians(d[5])), d[2]*np.cos(np.radians(d[4]))],
                      [0, d[1]*np.sin(np.radians(d[5])), -d[2]*np.sin(np.radians(d[4]))*np.cos(np.radians(d[3]))],
                      [0, 0, d[2]*np.sin(np.radians(d[4]))*np.sin(np.radians(d[3]))]])

        return M
    