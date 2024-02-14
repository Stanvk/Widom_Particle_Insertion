import time
import numpy as np
import MDAnalysis as md
import matplotlib.pyplot as plt
from datetime import datetime
from Widom.TestParticle import TestParticle
from Widom.Multiprocess import Multiprocess

class Widom:

    def __init__(self, test_particle: TestParticle, *, processes = 1):
        """
        Initialize the Widom class. Set the test-particle.

        @params: test_particle (TestParticle)
        @returns: self (Widom)
        """
        self._test_particle = test_particle
        self._n_processes = processes
        self.insertion_energies = np.array([])

    @staticmethod
    def lennard_jones_potential(dist: np.array, epsilon: np.array, sigma: np.array):
        """
        Calculate LJ potential by the 12/6 LJ function. Supports matrix-matrix arithmetics for fast bulk calculations.

        @params: dist (np.array), epsilon (np.array), sigma (np.array)
        @returns: (np.array)
        """
        # c6 = 4*epsilon*sigma**6
        # c12 = 4*epsilon*sigma**12
        
        return 4*epsilon*((sigma/dist)**(12)-(sigma/dist)**6)
    
    @staticmethod
    def lennard_jones_correction_term(cut_off_radius, epsilon, sigma, volume):
        """
        Calculate the correction term for the Lennard-Jones potential energy, according to "Solubilities of small molecules in polyethylene evaluated by
        a test-particle-insertion method" from Fukuda, 2000.
        
        @params: cut_off_radius (mixed), epsilon (mixed), sigma (mixed), volume (mixed)
        @returns: correction term (mixed)
        """
        c6 = 4*epsilon*sigma**6
        c12 = 4*epsilon*sigma**12

        return (4/9)*(np.pi/volume)*(c12/(cut_off_radius**9)-3*c6/(cut_off_radius**3))
    
    @staticmethod
    def _compose_combined_LJ_params(epsilon_tp, sigma_tp, epsilons, sigmas) -> list:
        """
        Compose combined LJ parameters according to Lorentz-Berthelot combination rules.

        @params: epislon_tp (float), sigma_tp (float), epsilons (list), sigmas (list)
        @returns: [combined_epsilons, combined_sigmas] (list)
        """
        combined_sigmas = np.array(0.5*(sigma_tp+sigmas))
        combined_epsilons = np.array(np.sqrt(epsilon_tp*epsilons))

        return [combined_epsilons, combined_sigmas]
    
    def _defined_atomtypes(self):
        """
        Give a list of all the atoms that we're interested in.

        @params: None
        @returns: list of atomtypes (list)
        @raises: KeyError
        """

        try:
            if len(self._LJ_params.keys()) == 0:
                raise KeyError("LJ_params dict is empty!")
            
            return self._LJ_params.keys()
        except:
            raise KeyError("LJ_params dict does not exist!")
    
        
    def _get_LJ_params_from_sample(self, ag: md.AtomGroup) -> list:
        """
        Construct a list with all the epsilons and sigmas for each atom in the sample.

        @params: ag (md.AtomGroup)
        @returns: [epsilons, sigmas] (list)
        """

        epsilons = np.array([self._LJ_params[atomtype][0] for atomtype in ag.types])
        sigmas = np.array([self._LJ_params[atomtype][1] for atomtype in ag.types])

        return [epsilons, sigmas]

    def _calculate_LJ_energy(self, insertion_pos, ag: md.AtomGroup):
        """
        Calculate the total Lennard-Jones potential energy of the system.

        @params: insertion_pos
        @returns: lennard-jones potential for given insertion_pos
        """
        
        distances = np.linalg.norm(ag.positions - insertion_pos, axis=-1)

        distances[distances > self._test_particle.get_LJ_cutoff_radius()] = np.inf

        correction_term = self.lennard_jones_correction_term(self._test_particle.get_LJ_cutoff_radius(), self._combined_epsilons, self._combined_sigmas, self.volume).sum()
        return self.lennard_jones_potential(distances, self._combined_epsilons, self._combined_sigmas).sum() + correction_term
    
    def set_sample(self, sample: md.core.universe, LJ_params: dict):
        """
        Prepare the sample using MDAnalysis.

        @params: sample (MDAnalysis.core.universe), LJ_params (dict)
        @returns: self (Widom)
        """

        if set(sample.select_atoms('all').types) != set(LJ_params.keys()):
            raise KeyError('There are atoms in the sample that are not defined in the LJ parameters or vice versa!')

        self._sample = sample
        self._LJ_params = LJ_params

        return self
    
    def prepare(self, frame: int, number_of_insertions: int):
        """
        Prepare the atomgroup, calculate the volume of the simulation box and generate the insertion locations. After that calculate the combined Lennard Jones parameters for each couple

        @params: frame (int), number_of_insertions (int)
        @returns: self (Widom)
        """
        self._frame = frame
        self._sample.trajectory[frame]
        self._ag = self._sample.select_atoms('all', updating=True)

        xcoods = self._ag.positions[:,0]
        ycoods = self._ag.positions[:,1]
        zcoods = self._ag.positions[:,2]

        xmin, xmax = [np.min(xcoods), np.max(xcoods)]
        ymin, ymax = [np.min(ycoods), np.max(ycoods)]
        zmin, zmax = [np.min(zcoods), np.max(zcoods)]

        self.volume = self._ag.ts.volume
        self.number_of_insertions = number_of_insertions
        self.insertion_locations = np.random.rand(int(number_of_insertions), 3)*np.array([xmax-xmin, ymax-ymin, zmax-zmin])+np.array([xmin, ymin, zmin], dtype='float64')

        self._test_particle.initialize_positions(self.insertion_locations)

        return self
    
    def run(self):
        """
        Start the Widom Test Particle Insertion Analysis.

        @params: processes (int)
        @returns: (self)
        """
        self.write_log("Starting Widom Particle Insertion Analysis")
        self.write_log(str(self._n_processes) + " process(es) will be used!")
        starttime = time.time()

        governor = Multiprocess().load(self, n_processes=self._n_processes)
        governor.run()
        self.insertion_energies = governor.get_insertion_energies()
        # self.insertion_locations = governor.insertion_locations

        self._run_time = time.time() - starttime
        self.write_log('Finished! Analysis ran for ' + str(self._run_time) + ' seconds')

        return self
        
    def run_analysis(self):
        """
        Perform the actual insertions and calculate the LJ potential.
        
        @params:
        @returns: (self)
        """

        LJ_energies = np.zeros((self.number_of_insertions, len(self._test_particle.get_atomtypes())))

        for constituent in range(len(self._test_particle.get_atomtypes())):

            epsilons, sigmas = self._get_LJ_params_from_sample(self._ag)
            epsilon_tp, sigma_tp = self._test_particle.get_LJ_params()[constituent]
            self._combined_epsilons, self._combined_sigmas = self._compose_combined_LJ_params(epsilon_tp, sigma_tp, epsilons, sigmas)

            insertion_locations_consituent = self._test_particle.get_positions()[:,constituent,:]

            for i in range(self.number_of_insertions):

                LJ_energies[i, constituent] = self._calculate_LJ_energy(insertion_locations_consituent[i, :], self._ag)

        self.insertion_energies = LJ_energies.sum(axis=-1)

        return self
    
    def get_test_particle(self):

        return self._test_particle
    
    def get_frame(self):

        return self._frame
    
    def get_LJ_params(self):

        return self._LJ_params
    
    def get_sample(self):

        return self._sample
    
    def get_LJ_energies(self):
        """
        Return the Lennard-Jones insertion energies per insertion.

        @params: (None)
        @returns: LJ energies (np.array)
        """

        return self.insertion_energies
    
    def get_insertion_energies(self):
        """
        Return the insertion energies.

        @params:
        @returns: (np.array)
        """
        return self.get_LJ_energies()
    
    def get_insertion_locations(self):
        """
        Return insertion locations.

        @params:
        @returns: (np.array)
        """
        return self.insertion_locations
    
    def save_LJ_energies(self, path, stamp):
        """
        Helper function to save the LJ energies.

        @params: path (str), stamp (str)
        @returns: LJ_energies (np.array)
        """
        np.savetxt(path+'energies_'+stamp+'.txt', self.get_LJ_energies())

        return self.get_LJ_energies()
    
    def save_insertion_energies(self, path: str, stamp: str):
        """
        Save the insertion energies to a txt file.

        @params: path (str), stamp (str)
        @returns: (np.array)
        """
        return self.save_LJ_energies(path, stamp)
    
    def save_insertion_locations(self, path, stamp):
        """
        Save the insertion energies to a txt file.

        @params: path (str), stamp (str)
        @returns: (np.array)
        """
        np.savetxt(path+'locations_'+stamp+'.txt', self.get_insertion_locations())

        return self.get_insertion_locations()
    
    def get_moving_solubility(self, temperature: float):
        """
        Helper function to calculate the solubility coefficient based upon the Lennard-Jones insertion energy.

        @params: temperature (float)
        @returns rolling_mean (np.array)
        """
        Widom.write_log("Make sure the temperature is set correctly!")

        #dE kJ/mol
        R = 8.31446261815324/1000 #kJ / (K mol)
        T = temperature #K
        
        exp_de = np.exp(-self.get_insertion_energies()/(R*T))

        # return np.array([np.mean(exp_de[:i]) for i in range(1,len(dE))])
        return np.cumsum(exp_de)/np.arange(1, len(exp_de) + 1)
        # return np.convolve(exp_de, np.ones(w), 'valid') / w

    @staticmethod
    def write_log(message: str, flush=False):
        """
        Helper function to put a message out. For now it prints in the console

        @params: message (str)
        @returns: message (str)
        """
        print(message, flush=flush)
        
        return message