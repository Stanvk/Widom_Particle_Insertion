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

basepath = '/Users/stanvk/Projects/NTUA/systems/amorphous_pe/'
relative_outputpath = "Analysis/Widom/"

LJ_energies_files = glob.glob(basepath+relative_outputpath+'energies_*.txt')
print(LJ_energies_files)

solubilities = []
temperatures = []

for file in LJ_energies_files:
    pathname_length = len(basepath) + len(relative_outputpath)
    timestamp = file[pathname_length+9:pathname_length+26]

    print(timestamp)

    config = Container(basepath, relative_outputpath).load(filename='config_' + timestamp)
    # include_data = input('Include ' + timestamp + ', with ' + config.get('coordinate_file') + '? [y/N]')
    
    # if include_data == 'y':

    LJ_energies = np.loadtxt(file)
    R = 8.31446261815324/1000 #kJ / (K mol)
    T = config.get('temperature')
    S = np.mean(np.exp(-LJ_energies/(R*T)))
    
    # crystallinities.append(float(input('crystallinity')))
    temperatures.append(T)
    solubilities.append(S)

Plotter()

# Sort the arrays to their values
# temperatures, solubilities = np.array(temperatures), np.array(solubilities)
# temperatures_sorted_indices = temperatures.argsort()
# crystallinities = temperatures[temperatures_sorted_indices[::-1]]
# solubilities = solubilities[temperatures_sorted_indices[::-1]]

fit, cov = np.polyfit(temperatures, solubilities, deg=1, cov=True)
# fit2, cov2 = np.polyfit(temperatures[1:-1], solubilities[1:-1], deg=1, cov=True)

fit_errors = np.sqrt(np.diag(cov))
fit_x_data = np.linspace(298,450,100)
fit_y_data = fit_x_data*fit[0]+fit[1]

plt.plot(1000/temperatures, solubilities, 'o', label='Simulation data')
plt.plot(1000/fit_x_data, fit_y_data, label='Extrapolation')
# plt.plot(np.linspace(-0.05,0.4,100), fit[0]*np.linspace(-0.05,0.4,100)+fit[1], label='Linear fit')
# plt.plot(np.linspace(-0.05,0.4,100), fit2[0]*np.linspace(-0.05,0.4,100)+fit2[1], label='Linear fit, w/o first point')
# plt.plot(np.linspace(-0.05,0.4,100), 0.2916023555608961*(1-np.linspace(-0.05,0.4,100)), label=r'$S=S_a (1-\chi_c)$')
plt.ylabel(r'$S$ [-]')
plt.xlabel(r'$1000/T$ [K$^{-1}$]')
# plt.xlim(-0.05, 0.4)
plt.legend()
plt.yscale('log')
plt.savefig(config.output_path+'arrhenius_solubility_vs_temperature.pdf', format='pdf', bbox_inches='tight')
plt.show()

plt.cla()
plt.plot(temperatures, solubilities, 'o', label='Simulation data')
plt.plot(fit_x_data, fit_y_data, label='Extrapolation')
# plt.plot(np.linspace(-0.05,0.4,100), fit[0]*np.linspace(-0.05,0.4,100)+fit[1], label='Linear fit')
# plt.plot(np.linspace(-0.05,0.4,100), fit2[0]*np.linspace(-0.05,0.4,100)+fit2[1], label='Linear fit, w/o first point')
# plt.plot(np.linspace(-0.05,0.4,100), 0.2916023555608961*(1-np.linspace(-0.05,0.4,100)), label=r'$S=S_a (1-\chi_c)$')
plt.ylabel(r'$S$ [-]')
plt.xlabel(r'$T$ [K]')
# plt.xlim(-0.05, 0.4)
plt.legend()
plt.savefig(config.output_path+'solubility_vs_temperature.pdf', format='pdf', bbox_inches='tight')
plt.show()

# print('Regression coefficients:')
# print(fit)    
# print('Parameter uncertainties:')
# print(np.sqrt(np.diag(cov)))
