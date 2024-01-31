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

temperature = '280K'
simulation = 'sim1'
frame = 0
n_insertions = 10000

# basepath = '/Volumes/3MA60/md-ipp-transport/data/PPUA_20chains_2000mon/'+str(temperature)+'/'+str(simulation)+'/'
basepath = "/Volumes/3MA60/md-ipp-transport/data/TPI_testing_PPUA_2000mon/"
relative_outputpath = "Analysis/widom_insertion/with_corrections/"

config = Container(basepath, relative_outputpath)
config.set('basepath', basepath)
config.set('temperature', temperature)
config.set('simulation', simulation)
config.set('timestamp', timestamp)
config.set('n_insertions', n_insertions)
config.set('tpr_file', 'npt.tpr')
config.set('trajectory_file', 'npt.gro')

sample = md.Universe(basepath + config.get('tpr_file'), basepath + config.get('trajectory_file'))

config.set('frame', frame)
config.save(filename='config_'+str(timestamp)+'_frame_' + str(frame))

tpi = Widom(Dioxygen())
tpi.set_sample(sample, {'CH': [0.0828, 4.680], 'CH2': [0.3818, 3.950], 'CH3': [0.8139, 3.750]}) #iPP

tpi.prepare(frame = config.get('frame'), number_of_insertions = config.get('n_insertions'))
tpi.run()

print(tpi.get_LJ_energies())
np.save(config.output_path + 'LJ_energies_'+str(timestamp)+'_frame_'+str(frame)+'.npy', tpi.get_LJ_energies())

Plotter()

plt.plot(range(1,tpi.number_of_insertions), tpi.calculate_moving_solubility(float(temperature[:-2]), tpi.get_LJ_energies()))
plt.ylabel(r'$\langle \exp(-\beta \Delta E)\rangle_N$')
plt.xlabel(r'Iteration number $N$')
plt.savefig(config.output_path + 'chemical_potential_vs_insertions_'+str(timestamp)+'_frame_'+str(frame)+'.png')

plt.hist(tpi.get_LJ_energies(), range=(0))