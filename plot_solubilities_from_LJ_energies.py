import os
import sys
import glob
from datetime import datetime

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import numpy as np
import MDAnalysis as md
import matplotlib.pyplot as plt
from Helpers.Plotter import Plotter
from Helpers.Container import Container
from Widom.Widom import Widom

basepath = '/Users/stanvk/Projects/NTUA/systems/pe_configurations_298K/'
relative_outputpath = "Analysis/Widom/"

LJ_energies_files = glob.glob(basepath+relative_outputpath+'LJ_energies_*.txt')
print(LJ_energies_files)

for file in LJ_energies_files:
    pathname_length = len(basepath) + len(relative_outputpath)
    timestamp = file[pathname_length+12:pathname_length+29]

    config = Container(basepath, relative_outputpath).load(filename='config_'+timestamp)

    LJ_energies = np.loadtxt(file)
    moving_solubility = Widom.calculate_moving_solubility(config.get('temperature'), LJ_energies)

    Plotter()

    plt.plot(range(1,int(config.get('n_insertions'))), moving_solubility)
    plt.ylabel(r'$\langle \exp(-\beta \Delta E)\rangle_N$')
    plt.xlabel(r'Iteration number $N$')
    plt.savefig(config.output_path+'solubility_'+config.get_timestamp()+'.pdf', format='pdf', bbox_inches='tight')
