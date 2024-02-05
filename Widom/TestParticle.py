from abc import ABC, abstractmethod
import numpy as np

class TestParticle(ABC):

    def get_positions(self):

        return self._positions
    
    def initialize_positions(self, random_locations):

        self._positions = np.array([self._calculate_positions(random_location) for random_location in random_locations])

        return self

    def get_particle_name(self) -> str:
        
        return str(__class__)

    @abstractmethod
    def _calculate_positions(self) -> np.array:
        """
        Generate random positions for the test-particle constituents.
        """
        return
    
    @abstractmethod
    def get_LJ_params(self):
        return
    
    @abstractmethod
    def get_atomtypes(self):
        return
    
    @abstractmethod
    def get_LJ_cutoff_radius(self):
        return