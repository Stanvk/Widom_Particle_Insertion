import os
import sys
from datetime import datetime

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import numpy as np
import MDAnalysis as md
from Widom import Widom
from Dioxygen import Dioxygen
import matplotlib.pyplot as plt
from Extensions.Plotter import Plotter
from Analysis.Container import Container


timestamp = datetime.now().strftime("%d_%m_%Y_%H%M%S")

# basepath = '/Volumes/3MA60/md-ipp-transport/data/TPI_testing_PPUA_2000mon/'

temperature = '298K'
simulation = 'sim1'
frame = 0
n_insertions = 100000

basepath = '/Volumes/3MA60/md-ipp-transport/data/TPI_MDO_PE/trappe_corrected/'
relative_outputpath = "Analysis/widom_insertion/with_corrections_cut_off_14/"

config = Container(basepath, relative_outputpath)
config.set('basepath', basepath)
config.set('temperature', temperature)
config.set('simulation', simulation)
config.set('timestamp', timestamp)
config.set('n_insertions', n_insertions)
config.set('tpr_file', 'npt.tpr')
config.set('trajectory_file', 'npt.gro')

sample = md.Universe(basepath + 'pe.tpr', basepath + 'pe_trr_snapshot.gro')

config.set('frame', frame)
config.save(filename='config_'+str(timestamp)+'_frame_' + str(frame))

tpi = Widom(Dioxygen())
tpi.set_sample(sample, {'CH2': [0.38493, 3.950], 'CH3': [0.81588, 3.750]}) #PE

tpi.prepare(frame = config.get('frame'), number_of_insertions = config.get('n_insertions'))
tpi.run()

print(tpi.get_LJ_energies())

np.save(config.output_path + 'LJ_energies_'+str(timestamp)+'_frame_'+str(frame)+'.npy', tpi.get_LJ_energies())

Plotter()

plt.plot(range(1,tpi.number_of_insertions), tpi.calculate_moving_solubility(float(temperature[:-1]), tpi.get_LJ_energies()))
plt.ylabel(r'$\langle \exp(-\beta \Delta E)\rangle_N$')
plt.xlabel(r'Iteration number $N$')
plt.savefig(config.output_path + 'chemical_potential_vs_insertions_'+str(timestamp)+'_frame_'+str(frame)+'.png')

# import os
# import sys

# current = os.path.dirname(os.path.realpath(__file__))
# parent = os.path.dirname(current)
# sys.path.append(parent)

# import numpy as np
# import MDAnalysis as md
# from Widom import Widom
# from Dioxygen import Dioxygen
# import matplotlib.pyplot as plt
# from Analysis.Container import Container
# from Extensions.Plotter import Plotter

# basepath = '/Volumes/3MA60/md-ipp-transport/data/TPI_MDO_PE/trappe_corrected/'
# relative_outputpath = "Analysis/widom_insertion/with_corrections_cut_off_14/"

# number_of_insertions = 250000
# frame = 0


# config = Container(basepath, relative_outputpath)
# config.set('basepath', basepath)
# config.set('number_of_insertions', number_of_insertions)
# config.set('frame', frame)
# config.save()


# sample = md.Universe(basepath + 'pe.tpr', basepath + 'pe_trr_snapshot.gro')

# tpi = Widom(Dioxygen())
# tpi.set_sample(sample, {'CH2': [0.38493, 3.950], 'CH3': [0.81588, 3.750]}) #PE

# tpi.prepare(frame = frame, number_of_insertions = number_of_insertions)
# tpi.run()

# print(tpi.get_LJ_energies())

# np.save(config.output_path + 'LJ_energies.npy', tpi.get_LJ_energies())

# Plotter()

# plt.plot(range(1,tpi.number_of_insertions), tpi.calculate_moving_solubility(298, tpi.get_LJ_energies()))
# plt.ylabel(r'$\langle \exp(-\beta \Delta E)\rangle_N$')
# plt.xlabel(r'Iteration number $N$')
# plt.savefig(config.output_path + 'chemical_potential_vs_insertions.png')
# plt.show()