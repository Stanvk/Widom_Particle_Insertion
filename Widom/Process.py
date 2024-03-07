import MDAnalysis as md
from . import Widom
import time

class Process:

    @staticmethod
    def perform(id, queue_energies, queue_locations, test_particle, topology_file, coordinate_file, LJ_params, frame, n_insertions):
        Widom.Widom.write_log('Process '+str(id)+' started!')
        sample = md.Universe(topology_file, coordinate_file)

        tpi = Widom.Widom(test_particle)
        tpi.set_sample(sample, LJ_params)
        tpi.prepare(frame=frame, number_of_insertions=n_insertions)
        tpi.run_analysis()

        queue_energies.put(tpi.get_insertion_energies().tolist())
        queue_locations.put(tpi.get_insertion_locations().tolist())