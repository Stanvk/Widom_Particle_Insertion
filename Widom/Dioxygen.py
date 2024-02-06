from Widom.TestParticle import TestParticle
import numpy as np

class Dioxygen(TestParticle):

    def get_LJ_params(self):
        """
        Return an array where each row contains the LJ pair epsilon and sigma for the constituent for the testparticle

        @params: (None)
        @returns: (list)
        """
        # kJ/mol en Å
        return np.array([[0.40734, 3.02], [0.40734, 3.02]])
        # return np.array([[0.407409, 3.02], [0.407409, 3.02]]) # Values from Nikos used for testing.

    
    def get_LJ_cutoff_radius(self) -> float:
        """
        Retrieve the cut-off distance for the Lennard-Jones potential. The units are in Ångstroms (Å).

        params: (None)
        returns: Lennard-Jones cut-off radius in Ångstrom. (float)
        """
        # return 14 #angstrom
        return 9.09 #angstrom; values from Nikos used for testing
    
    def get_atomtypes(self):
        """
        Return an array that lists the atom type for each constituent.

        @params: (None)
        @returns: (list)
        """

        return np.array(['O','O'])
    
    @staticmethod
    def __transform_spherical_to_cartesian(r, theta, phi):
        """
        A static method that performs a coordinate transformations from spherical coordinates to cartesian ones.

        @params: r (float), theta (float), phi (float)
        @returns: cartesian coordinates (np.array)
        """
        x = r * np.sin(theta, dtype=np.float64) * np.cos(phi, dtype=np.float64)
        y = r * np.sin(theta, dtype=np.float64) * np.sin(phi, dtype=np.float64)
        z = r * np.cos(theta, dtype=np.float64)

        return np.array([x, y, z])

    def _calculate_positions(self, center) -> np.array:
        """
        Give the positions of the test-particle constituents.

        @params: (None)
        @returns: Coordinates (np.array)
        """
        l = 1.21 # Angstrom

        phi = np.arccos(2*np.random.rand(1).astype(np.float64)[0]-1) # polar angle
        theta = 2*np.pi*np.random.rand(1).astype(np.float64)[0] # azimuthal angle
        r = l/2 # radius in angstrom

        part = Dioxygen.__transform_spherical_to_cartesian(r, theta, phi)

        # return np.array([[4.687089599, 12.8870504, 53.88286897],[5.182721359, 13.03486294, 52.78897656]]) # insertion 1 of Omar
        # return np.array([[34.11453381, 7.6544122, 116.5455118],[34.81119064, 7.750164678, 117.5301949]]) # insertion 2 of Omar
        # return np.array([[33.82512735, 6.431934709, 75.96615388],[32.95696881, 6.164926415, 76.76559576]]) # insertion 3 of Omar
        # return np.array([[23.92219826, 12.18719422, 86.64278244],[24.26723019, 11.78584686, 87.73088779]]) # insertion 4 of Omar
        # return np.array([[60.36825102, 17.23110917, 2.207646596],[60.96426553, 16.22642367, 2.523041194]]) # insertion 5 of Omar

        # return np.array([[66.99,115.04,09.61],[67.93,114.32,09.86]]) # insertion 3 of Nikos
        # return np.array([[61.27, 7.46, 29.71], [61.47, 7.22, 28.54]]) # insertion 2 of Nikos
        
        # return np.array([[65.71, 117.00, 65.03],[65.20, 116.58, 66.04]]) # test particle 1
        # return np.array([[66.98,47.27,97.48], [67.10,47.24,98.68]]) # test particle 2
        # return np.array([[57.02, 73.07, 76.28],[56.26, 72.19, 76.59]])

        return np.array([center+part, center-part]) 