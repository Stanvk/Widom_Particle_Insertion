import matplotlib.pyplot as plt
import numpy as np
from Helpers.Container import Container
import MDAnalysis as md
from datetime import datetime
# from Widom.TestParticle import TestParticle
from Widom.Widom import Widom
from Widom.Dioxygen import Dioxygen
from Helpers.Plotter import Plotter

# basepath = '/Users/stanvk/Downloads/pe_configurations_450K/C1K2000000000/'
basepath = '/Users/stanvk/Projects/NTUA/systems/validation_system_omar/'
# basepath = '/Users/stanvk/Downloads/'
# relative_path = 'Analysis/widom_insertion/dioxygen/'

timestamp = datetime.now().strftime("%d_%m_%Y_%H%M%S")

sample = md.Universe(basepath+'pe.tpr', basepath+'pe.gro')
# sample = md.Universe(basepath+'npt_ipp_320K.gro', basepath+'npt_ipp_320K.gro')

ag = sample.select_atoms('all')

print(ag.names)
print(ag.types)

# config = Container(basepath, relative_outputpath)
# config.set('basepath', basepath)
# config.set('relative_outputpath',relative_outputpath)
# config.set('temperature', temperature)
# config.set('simulation', simulation)
# config.set('timestamp', timestamp)
# config.set('frame_series', np.arange(0,len(sample.trajectory),1).tolist())
# config.set('n_iterations', 1e6)
# config.set('frame', 0)
# config.save(filename='config_'+str(timestamp)+'_frame_'+str(frame))

tpi = Widom(Dioxygen())
tpi.set_sample(sample, {'CH2': [0.38493, 3.950], 'CH3': [0.81588, 3.750]})
# tpi.set_sample(sample, {'CH': [0.0828, 4.680], 'CH2': [0.3818, 3.950], 'CH3': [0.8139, 3.750]}) #iPP

# tpi.prepare(frame = config.get('frame'), number_of_insertions = config.get('n_insertions'))
tpi.prepare(frame=0, number_of_insertions=200000)
tpi.run()

# np.save(config.output_path + 'LJ_energies_'+str(timestamp)+'_frame_'+str(frame)+'.npy', tpi.get_LJ_energies())

Plotter()

print(tpi.get_LJ_energies())
plt.plot(tpi.get_LJ_energies())
plt.show()

plt.plot(range(1,tpi.number_of_insertions), tpi.calculate_moving_solubility(450, tpi.get_LJ_energies()))
plt.ylabel(r'$\langle \exp(-\beta \Delta E)\rangle_N$')
plt.xlabel(r'Iteration number $N$')
plt.show()