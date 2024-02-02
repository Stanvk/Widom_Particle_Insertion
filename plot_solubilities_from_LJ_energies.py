import os
import sys
import glob
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

temperature = '280K'
simulation = 'sim1'

basepath = '/Volumes/3MA60/md-ipp-transport/data/PPUA_20chains_2000mon/'+str(temperature)+'/'+str(simulation)+'/'
relative_outputpath = "Analysis/widom_insertion/with_corrections/"

LJ_energies_files = glob.glob(basepath+relative_outputpath+'LJ_energies_*.npy')
print(LJ_energies_files)

for file in LJ_energies_files:
    pathname_length = len(basepath) + len(relative_outputpath)
    
    dE = np.load(file)
    timestamp = file[pathname_length+12:pathname_length+29]
    frame = file[pathname_length+36:-4]

    dynamic_avg_exp_dE = Widom.calculate_moving_solubility(float(temperature[:-1]), dE)

    np.savetxt(basepath + relative_outputpath + 'dynamic_avg_exp_dE_'+str(timestamp)+'.txt', dynamic_avg_exp_dE)

    Plotter()

    plt.plot(range(1,len(dE)), dynamic_avg_exp_dE)
    plt.ylabel(r'$\langle \exp(-\beta \Delta E)\rangle_N$')
    plt.xlabel(r'Iteration number $N$')
    plt.savefig(basepath + relative_outputpath + 'chemical_potential_vs_insertions_'+str(timestamp)+'.png')