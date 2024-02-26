import os
import sys
import glob

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import numpy as np
import MDAnalysis as md
import matplotlib.pyplot as plt
from Helpers.Plotter import Plotter
from Helpers.Container import Container
from Widom.Widom import Widom

# basepath = '/Users/stanvk/Projects/NTUA/systems/alpha_phase_iPP/UA_FF/'
basepath = '/Users/stanvk/Projects/NTUA/systems/ipp_semicrystalline/410K/500ns/'
# basepath = '/Users/stanvk/Projects/NTUA/systems/alpha_phase_iPP/'
# basepath = '/Users/stanvk/Projects/NTUA/systems/pe_configurations_298K/'
relative_outputpath = "Analysis/Widom/"

LJ_energies_files = glob.glob(basepath+relative_outputpath+'energies*.txt')
print(LJ_energies_files)

for file in LJ_energies_files:
    pathname_length = len(basepath) + len(relative_outputpath)
    timestamp = file[pathname_length+9:pathname_length+26]
    print(timestamp)

    config = Container(basepath, relative_outputpath).load(filename='config_'+timestamp)

    LJ_energies = np.loadtxt(file)
    moving_solubility = Widom.get_moving_solubility(config.get('temperature'), LJ_energies)
    converged_solubility = moving_solubility[-1]

    Plotter()

    plt.plot(range(1,int(config.get('n_insertions')+1)), moving_solubility)
    xmin, xmax = plt.gca().get_xlim()
    plt.hlines(converged_solubility, xmin=xmin, xmax=xmax)
    plt.title('S = ' + str(converged_solubility))
    plt.ylabel(r'$\langle \exp(-\beta \Delta E)\rangle_N$')
    plt.xlabel(r'$\mathrm{Iteration}$ $N$')
    plt.savefig(config.output_path+'solubility_'+config.get_timestamp()+'.pdf', format='pdf', bbox_inches='tight')
    plt.close()
