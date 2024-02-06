import matplotlib.pyplot as plt
import numpy as np
from Helpers.Container import Container
import MDAnalysis as md
from datetime import datetime
from Widom.Widom import Widom
from Widom.Dioxygen import Dioxygen
from Helpers.Plotter import Plotter

basepath = '/Users/stanvk/Projects/NTUA/systems/pe_configurations_280K/'
relative_outputpath = 'Analysis/Widom/'

sample = md.Universe(basepath+'pe.tpr', basepath+'amorphous.gro')

config = Container(basepath, relative_outputpath)
config.set('basepath', basepath)
config.set('relative_outputpath',relative_outputpath)
config.set('temperature', 298)
config.set('frame_series', np.arange(0,len(sample.trajectory),1).tolist())
config.set('n_iterations', 1e6)
config.set('frame', 0)
config.set('test_particle', 'Dioxygen')
config.set('LJ_params_solvent', {'CH2': [0.38493, 3.950], 'CH3': [0.81588, 3.750]})
# {'CH': [0.0828, 4.680], 'CH2': [0.3818, 3.950], 'CH3': [0.8139, 3.750]}
config.save(filename='config_'+config.get_timestamp()+'.txt')

tpi = Widom(Dioxygen())
tpi.set_sample(sample, config.get('LJ_params_solvent'))

tpi.prepare(frame=config.get('frame'), number_of_insertions=config.get('n_iterations'))
tpi.run()

Plotter()

tpi.save_LJ_energies(config.output_path, config.get_timestamp())

plt.hist(tpi.get_LJ_energies())
plt.xlabel(r'$\mathrm{Insertion}$ $\mathrm{energy}$ [$\mathrm{kJ} \mathrm{mol}^{-1}$]')
plt.ylabel(r'$\mathrm{Frequency}$')
plt.savefig(config.output_path+'LJ_energies_histogram_'+config.get_timestamp()+'.pdf', format='pdf', bbox_inches='tight')
plt.close()

plt.plot(range(1,tpi.number_of_insertions), tpi.calculate_moving_solubility(config.get('temperature'), tpi.get_LJ_energies()))
plt.ylabel(r'$\langle \exp(-\beta \Delta E)\rangle_N$')
plt.xlabel(r'Iteration number $N$')
plt.savefig(config.output_path+'solubility_'+config.get_timestamp()+'.pdf', format='pdf', bbox_inches='tight')
