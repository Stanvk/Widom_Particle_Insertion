import matplotlib.pyplot as plt
import numpy as np
from Helpers.Container import Container
import MDAnalysis as md
from Widom.Widom import Widom
from Widom.Dioxygen import Dioxygen
from Helpers.Plotter import Plotter

basepath = '/Users/stanvk/Projects/NTUA/systems/amorphous_pe/'
relative_outputpath = 'Analysis/Widom_test/'

# config = Container(basepath, relative_outputpath).load(filename=config_file)
config = Container(basepath, relative_outputpath)

config.set('topology_file', 'pe.tpr')
config.set('coordinate_file', 'amorphous_350K.gro')

sample = md.Universe(basepath+config.get('topology_file'), basepath+config.get('coordinate_file'))

config.set('test_particle', 'Dioxygen')
config.set('frame_series', np.arange(0,len(sample.trajectory),1).tolist())
config.set('n_insertions_per_frame', 1000)
config.set('LJ_params_solvent', {'CH2': [0.38493, 3.950], 'CH3': [0.81588, 3.750]}) #PE (TraPPE)
config.save(filename='config_'+config.get_timestamp())

for ts in sample.trajectory:
    tpi = Widom(Dioxygen(), processes=4)
    tpi.set_sample(sample, config.get('LJ_params_solvent'))
    tpi.prepare(frame=ts.frame, number_of_insertions=config.get('n_insertions_per_frame'))    

    if __name__ == '__main__':
        tpi.run()

        tpi.save_insertion_energies(config.output_path, config.get_timestamp()+'_frame_'+str(ts.frame))
        tpi.save_insertion_locations(config.output_path, config.get_timestamp()+'_frame_'+str(ts.frame))
        
        del tpi