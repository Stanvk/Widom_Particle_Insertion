import MDAnalysis as md
from . import Widom
import time

class Process:

    @staticmethod
    def perform(id, queue_energies, queue_locations, test_particle, topology_file, coordinate_file, LJ_params, frame, n_insertions):

        sample = md.Universe(topology_file, coordinate_file)

        # print('Process ' +str(id)+' running!', flush=True)

        starttime = time.time()

        tpi = Widom.Widom(test_particle)
        tpi.set_sample(sample, LJ_params)
        tpi.prepare(frame=frame, number_of_insertions=n_insertions)
        tpi.run_analysis()

        runtime = time.time()-starttime
        # print('Process ' + str(id) + ' finished in ' + str(runtime) + 's.', flush=True)

        queue_energies.put(tpi.get_insertion_energies().tolist())

        # print('Process ' +str(id)+' queued insertion energies!', flush=True)

        queue_locations.put(tpi.get_insertion_locations().tolist())

        # print('Process ' +str(id)+' queued insertion locations!', flush=True)