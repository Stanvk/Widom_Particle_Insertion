import MDAnalysis.core.universe as universe
import numpy as np

class TimeSeries:

    def __init__(self, u: universe):

        self.u = u
        self.n_frames = self.u.trajectory.n_frames
        self.dt = self.u.trajectory.dt

        self._loop_through_traj()

    def get_frames(self) -> list:
        
        return self.frames.tolist()
    
    def get_times(self) -> list:

        return self.times.tolist()

    def _loop_through_traj(self):
        
        self.u.trajectory[0]

        self.frames = np.arange(0,self.n_frames,1)
        self.times = self.frames*self.dt #ps

        return self