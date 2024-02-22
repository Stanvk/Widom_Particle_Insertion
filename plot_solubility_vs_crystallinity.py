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

LJ_energies_files = glob.glob(basepath+relative_outputpath+'energies_*.txt')
print(LJ_energies_files)

solubilities = []
crystallinities = []
temperatures = []

for file in LJ_energies_files:
    pathname_length = len(basepath) + len(relative_outputpath)
    timestamp = file[pathname_length+9:pathname_length+26]

    print(timestamp)

    config = Container(basepath, relative_outputpath).load(filename='config_' + timestamp)
    # include_data = input('Include ' + timestamp + ', with ' + config.get('coordinate_file') + '? [y/N]')
    
    # if include_data == 'y':

    if not config.exists('temperature') or not config.exists('crystallinity'):
        print('Temperature or crystallinity is not defined in configuration file: config_' + str(config.get_timestamp()))
        continue

    dE = np.loadtxt(file)
    R = 8.31446261815324/1000 #kJ / (K mol)
    T = config.get('temperature')
    S = np.mean(np.exp(-dE/(R*T)))
    
    # crystallinities.append(float(input('crystallinity')))
    
    solubilities.append(S)
    crystallinities.append(config.get('crystallinity'))
    temperatures.append(T)

Plotter()

# Sort the arrays to their values
# temperatures, solubilities = np.array(temperatures), np.array(solubilities)
# temperatures_sorted_indices = temperatures.argsort()
# crystallinities = temperatures[temperatures_sorted_indices[::-1]]
# solubilities = solubilities[temperatures_sorted_indices[::-1]]

crystallinities = np.array(crystallinities)/100
temperatures = np.array(temperatures)
solubilities = np.array(solubilities)

fit, cov = np.polyfit(crystallinities, solubilities, deg=1, cov=True)

fit_x_data = np.linspace(-0.05,0.5,100)
fit_y_data = fit[0]*fit_x_data+fit[1]
fit_errors = np.sqrt(np.diag(cov))
fit_y_error_neg = (fit[0]-fit_errors[0])*fit_x_data+(fit[1]-fit_errors[1])
fit_y_error_pos = (fit[0]+fit_errors[0])*fit_x_data+(fit[1]+fit_errors[1])

plt.scatter([0.3137857678, 0.3153318352, 0.2929348315, 0.2598681648], np.array([0.028655128, 0.007973945, 0.026293091, 0.045982144]), marker='s', label='Kurek et al.')
plt.plot(crystallinities, solubilities, 'o', label='Simulation data')
plt.plot(fit_x_data, fit_y_data, label='Linear fit')
plt.fill_between(fit_x_data, fit_y_error_neg, fit_y_error_pos, color='blue', alpha=0.3)
plt.plot(np.linspace(-0.05,0.5,100), 0.2916023555608961*(1-np.linspace(-0.05,0.4,100)), label=r'$S=S_a (1-\chi_c)$')
plt.ylabel(r'$S$ $[-]$')
plt.xlabel(r'$\chi_C$ $[-]$')
plt.xlim(np.min(fit_x_data), np.max(fit_x_data))
plt.legend()
# plt.savefig(config.output_path+'arrhenius_solubility_vs_temperature.pdf', format='pdf', bbox_inches='tight')
plt.show()