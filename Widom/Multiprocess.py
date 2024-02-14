import multiprocessing
import numpy as np
from Widom.Process import Process


class Multiprocess:

    def __init__(self):
        """
        Initiate the Multiprocess governor.
        """
        self._processes = []
        self._subinstances = []
        self._insertion_locations = []
        self._insertion_energies = []

    def load(self, instance, n_processes: int):
        """
        Load the Widom class and prepare subprocesses.

        @params: instance (Widom), n_processes (int)
        @returns: self (Multiprocess)

        """
        self._widom = instance
        self._n_processes = n_processes
        self._n_insertions_per_subprocess = int(instance.number_of_insertions / self._n_processes)
        self._queues_energies = []
        self._queues_locations = []
    
        return self

    def run(self):
        """
        Run the Widom class across multiple processes.

        @params: 
        @returns: self (Multiprocess)

        """

        for i in range(self._n_processes):
            self._queues_energies.append(multiprocessing.Queue())
            self._queues_locations.append(multiprocessing.Queue())

            p = multiprocessing.Process(target=Process.perform, args=(
                    i, self._queues_energies[i],
                    self._queues_locations[i],
                    self._widom.get_test_particle(),
                    self._widom.get_sample().filename,
                    self._widom.get_sample().trajectory.filename,
                    self._widom.get_LJ_params(),
                    self._widom.get_frame(),
                    self._n_insertions_per_subprocess
                ))
            
            self._processes.append(p)
            p.start()

        [p.join() for p in self._processes]

        print('Processes finalized!')

        self._insertion_energies = [q.get() for q in self._queues_energies]
        self._insertion_locations = [q.get() for q in self._queues_locations]

        return self
    
    def get_insertion_energies(self):
        """
        Return concatenated insertion energies.

        @params:
        @returns: (np.array)
        """
        return np.array(self._insertion_energies).flatten()
    
    def get_insertion_locations(self):
        """
        Return concatenated insertion locations

        @params:
        @returns: (np.array)
        """
        return np.array(self._insertion_locations).flatten()






        