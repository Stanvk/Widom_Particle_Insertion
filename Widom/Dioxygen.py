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

        @params: (None)
        @returns: Lennard-Jones cut-off radius in Ångstrom. (float)
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

        return np.array([center+part, center-part]) 