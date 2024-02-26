import numpy as np
from Widom.Coordinates import Coordinates
import MDAnalysis as md

basepath = '/Users/stanvk/Projects/NTUA/systems/alpha_phase_iPP/hybrid_FF_equilibrated/'
relative_output = 'Analysis/Widom/'

file = 'locations_26_02_2024_155108.txt'

pos = np.loadtxt(basepath+relative_output+file)

u = md.Universe.empty(len(pos), trajectory=True)
u.atoms.positions = pos

u.atoms.write(basepath+relative_output+file[:-4]+'.gro', reindex=False)
