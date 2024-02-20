import matplotlib.pyplot as plt
import numpy as np
from Helpers.Container import Container
import MDAnalysis as md
from Widom.Widom import Widom
from Widom.Dioxygen import Dioxygen
from Helpers.Plotter import Plotter
from MDAnalysis.lib.mdamath import triclinic_vectors
from Helpers.Coordinates import Coordinates

basepath = '/Users/stanvk/Projects/NTUA/systems/alpha_phase_iPP/'
relative_outputpath = 'Analysis/Widom/'

sample = md.Universe(basepath+'npt.tpr', basepath+'dump.gro')

print(sample.dimensions)

points = np.random.rand(int(1e5),3)

# T = triclinic_vectors(sample.dimensions)
T = Coordinates.triclinic_transformation(sample.dimensions)

# transformed_points = []

# for point in points:
#     transformed_points.append(np.dot(T, point))

# transformed_points = np.array(transformed_points)

transformed_points = np.einsum('ij,kj->ki',T,points)

u = md.Universe.empty(int(1e5), trajectory=True) 

u.atoms.positions = transformed_points

# Save to .gro file
u.atoms.write(basepath+"T.gro")